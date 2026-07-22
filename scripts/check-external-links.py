#!/usr/bin/env python3
"""Bounded HTTPS link check with DNS and redirect SSRF protections."""

from __future__ import annotations

import argparse
import concurrent.futures
import ipaddress
import re
import shutil
import socket
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit


INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)(?:\s+[^)]*)?\)")
REFERENCE_LINK_RE = re.compile(
    r"^\s*\[[^\]]+\]:\s*<?(https?://[^>\s]+)>?", re.MULTILINE
)
REDIRECT_CODES = {301, 302, 303, 307, 308}
REACHABLE_DENIAL_CODES = {401, 403, 405, 429}
MAX_URLS = 75
MAX_REDIRECTS = 3
MAX_WORKERS = 8
CONNECT_TIMEOUT_SECONDS = 4
REQUEST_TIMEOUT_SECONDS = 8


class LinkError(Exception):
    pass


@dataclass(frozen=True)
class CheckResult:
    source: str
    url: str
    ok: bool
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check public Markdown HTTPS links without allowing private-network requests."
    )
    parser.add_argument("repo_root", nargs="?", default=".")
    return parser.parse_args()


def markdown_paths(repo_root: Path) -> list[Path]:
    paths = [repo_root / name for name in ("README.md", "CONTRIBUTING.md", "SECURITY.md")]
    paths.extend((repo_root / "skills").rglob("*.md"))
    return sorted(
        path for path in paths if path.is_file() and not path.is_symlink()
    )


def collect_links(repo_root: Path) -> list[tuple[str, str]]:
    seen: set[str] = set()
    links: list[tuple[str, str]] = []
    for path in markdown_paths(repo_root):
        contents = path.read_text(encoding="utf-8")
        urls = [match.group(1) for match in INLINE_LINK_RE.finditer(contents)]
        urls.extend(match.group(1) for match in REFERENCE_LINK_RE.finditer(contents))
        for url in urls:
            if url in seen:
                continue
            seen.add(url)
            links.append((path.relative_to(repo_root).as_posix(), url))
    if len(links) > MAX_URLS:
        raise LinkError(
            f"refusing to check {len(links)} unique URLs; the fixed safety limit is {MAX_URLS}"
        )
    return links


def validate_and_resolve(url: str) -> tuple[str, str, str]:
    if len(url) > 2048:
        raise LinkError("URL exceeds 2,048 characters")
    if "\\" in url or any(ord(character) <= 0x20 for character in url):
        raise LinkError("URL contains whitespace, control characters, or backslashes")
    parsed = urlsplit(url)
    if parsed.scheme != "https":
        raise LinkError("only HTTPS links are eligible for network checks")
    if not parsed.hostname:
        raise LinkError("URL has no hostname")
    if parsed.username is not None or parsed.password is not None:
        raise LinkError("URLs containing credentials are forbidden")
    try:
        port = parsed.port
    except ValueError as exc:
        raise LinkError(f"invalid port: {exc}") from exc
    if port not in (None, 443):
        raise LinkError("only the standard HTTPS port is allowed")

    try:
        hostname = parsed.hostname.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise LinkError(f"hostname is not valid IDNA: {exc}") from exc
    if hostname == "localhost" or hostname.endswith(".localhost") or hostname.endswith(".local"):
        raise LinkError("local hostnames are forbidden")

    try:
        records = socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise LinkError(f"DNS resolution failed: {exc}") from exc
    addresses = sorted(
        {record[4][0] for record in records},
        key=lambda address: (ipaddress.ip_address(address).version != 4, address),
    )
    if not addresses:
        raise LinkError("DNS returned no addresses")
    for address in addresses:
        parsed_address = ipaddress.ip_address(address)
        if not parsed_address.is_global:
            raise LinkError(f"DNS returned forbidden non-global address {address}")

    # Pin curl to one address after validating every DNS result. --noproxy
    # prevents an ambient proxy from bypassing that pin.
    normalized_host = f"[{hostname}]" if ":" in hostname else hostname
    normalized_url = urlunsplit(
        (parsed.scheme, normalized_host, parsed.path, parsed.query, parsed.fragment)
    )
    return hostname, addresses[0], normalized_url


def curl_request(url: str, method: str) -> tuple[int, str | None]:
    hostname, address, normalized_url = validate_and_resolve(url)
    pinned_address = f"[{address}]" if ":" in address else address
    command = [
        "curl",
        "--disable",
        "--silent",
        "--show-error",
        "--noproxy",
        "*",
        "--proto",
        "=https",
        "--proto-redir",
        "=https",
        "--connect-timeout",
        str(CONNECT_TIMEOUT_SECONDS),
        "--max-time",
        str(REQUEST_TIMEOUT_SECONDS),
        "--max-redirs",
        "0",
        "--resolve",
        f"{hostname}:443:{pinned_address}",
        "--user-agent",
        "jimmyhoran-skills-link-check/1.0",
        "--dump-header",
        "-",
        "--output",
        "/dev/null",
        "--write-out",
        "\n__LINK_STATUS__:%{http_code}\n",
    ]
    if method == "HEAD":
        command.extend(["--head"])
    else:
        command.extend(["--range", "0-0"])
    command.append(normalized_url)

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=REQUEST_TIMEOUT_SECONDS + 2,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"curl exited {completed.returncode}"
        raise LinkError(detail)
    status_match = re.search(r"__LINK_STATUS__:(\d{3})", completed.stdout)
    if status_match is None:
        raise LinkError("curl returned no HTTP status")
    status = int(status_match.group(1))
    location: str | None = None
    for line in completed.stdout.splitlines():
        if line.lower().startswith("location:"):
            location = line.split(":", 1)[1].strip()
    return status, location


def check_url(source: str, original_url: str) -> CheckResult:
    current_url = original_url
    try:
        for redirect_count in range(MAX_REDIRECTS + 1):
            status, location = curl_request(current_url, "HEAD")
            if status == 405:
                status, location = curl_request(current_url, "GET")
            if status in REDIRECT_CODES:
                if not location:
                    raise LinkError(f"HTTP {status} redirect has no Location header")
                if redirect_count == MAX_REDIRECTS:
                    raise LinkError(f"exceeded {MAX_REDIRECTS} redirects")
                redirected = urljoin(current_url, location)
                parsed_redirect = urlsplit(redirected)
                current_url = urlunsplit(
                    (
                        parsed_redirect.scheme,
                        parsed_redirect.netloc,
                        parsed_redirect.path,
                        parsed_redirect.query,
                        "",
                    )
                )
                # Validate before the next request so unsafe redirects fail
                # without ever reaching curl.
                validate_and_resolve(current_url)
                continue
            if 200 <= status < 300:
                return CheckResult(source, original_url, True, f"HTTP {status}")
            if status in REACHABLE_DENIAL_CODES:
                return CheckResult(
                    source,
                    original_url,
                    True,
                    f"HTTP {status} (endpoint reachable; automated check denied or limited)",
                )
            raise LinkError(f"HTTP {status}")
        raise LinkError("redirect loop")
    except (LinkError, OSError, subprocess.SubprocessError, ValueError) as exc:
        return CheckResult(source, original_url, False, str(exc))


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.is_dir():
        print(f"error: repository root is not a directory: {repo_root}", file=sys.stderr)
        return 2
    if shutil.which("curl") is None:
        print("error: curl is required", file=sys.stderr)
        return 2
    try:
        links = collect_links(repo_root)
    except (LinkError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not links:
        print("No external Markdown links found.")
        return 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_url, source, url) for source, url in links]
        results = sorted((future.result() for future in futures), key=lambda item: item.url)

    failures = 0
    for result in results:
        marker = "ok" if result.ok else "FAIL"
        print(f"[{marker}] {result.url} ({result.source}) - {result.detail}")
        if not result.ok:
            failures += 1
    print(f"Checked {len(results)} unique external links; {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
