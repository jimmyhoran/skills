#!/usr/bin/env python3
"""Offline negative fixtures for the external-link SSRF boundary."""

from __future__ import annotations

import importlib.util
import socket
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


def load_checker(script_path: Path) -> ModuleType:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("external_link_checker", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def dns_records(*addresses: str) -> list[tuple[Any, ...]]:
    records: list[tuple[Any, ...]] = []
    for address in addresses:
        family = socket.AF_INET6 if ":" in address else socket.AF_INET
        endpoint: tuple[Any, ...]
        if family == socket.AF_INET6:
            endpoint = (address, 443, 0, 0)
        else:
            endpoint = (address, 443)
        records.append((family, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", endpoint))
    return records


def require_link_error(checker: ModuleType, label: str, operation: Callable[[], Any]) -> None:
    try:
        operation()
    except checker.LinkError:
        print(f"[ok] rejected {label}")
        return
    raise AssertionError(f"{label}: unsafe URL unexpectedly passed")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    checker = load_checker(repo_root / "scripts" / "check-external-links.py")

    require_link_error(
        checker,
        "plain HTTP",
        lambda: checker.validate_and_resolve("http://example.com/"),
    )
    require_link_error(
        checker,
        "URL credentials",
        lambda: checker.validate_and_resolve("https://user:token@example.com/"),
    )
    require_link_error(
        checker,
        "non-standard HTTPS port",
        lambda: checker.validate_and_resolve("https://example.com:8443/"),
    )
    require_link_error(
        checker,
        "loopback literal",
        lambda: checker.validate_and_resolve("https://127.0.0.1/"),
    )
    require_link_error(
        checker,
        "URL backslash",
        lambda: checker.validate_and_resolve("https://example.com\\@127.0.0.1/"),
    )

    original_getaddrinfo = checker.socket.getaddrinfo
    checker.socket.getaddrinfo = lambda *args, **kwargs: dns_records(
        "93.184.216.34", "10.0.0.7"
    )
    require_link_error(
        checker,
        "mixed public and private DNS",
        lambda: checker.validate_and_resolve("https://example.com/"),
    )

    checker.socket.getaddrinfo = original_getaddrinfo
    original_curl_request = checker.curl_request
    checker.curl_request = lambda url, method: (302, "https://169.254.169.254/latest/meta-data")
    redirect_result = checker.check_url("fixture.md", "https://example.com/")
    if redirect_result.ok or "non-global" not in redirect_result.detail:
        raise AssertionError("private-address redirect was not rejected before a second request")
    print("[ok] rejected redirect to link-local metadata address")
    checker.curl_request = original_curl_request

    captured_command: list[str] = []

    class Completed:
        returncode = 0
        stdout = "HTTP/1.1 200 OK\r\n\r\n__LINK_STATUS__:200\n"
        stderr = ""

    def fake_run(command: list[str], **kwargs: Any) -> Completed:
        del kwargs
        captured_command.extend(command)
        return Completed()

    checker.socket.getaddrinfo = lambda *args, **kwargs: dns_records("93.184.216.34")
    checker.subprocess.run = fake_run
    status, _ = checker.curl_request("https://example.com/health", "HEAD")
    if status != 200:
        raise AssertionError("pinned curl fixture did not return its synthetic status")
    required_arguments = {
        "--disable",
        "--noproxy",
        "--resolve",
        "example.com:443:93.184.216.34",
    }
    if not required_arguments.issubset(captured_command) or "--location" in captured_command:
        raise AssertionError(f"curl request lost its pinned no-proxy boundary: {captured_command}")
    print("[ok] curl is pinned to a validated address with proxies and auto-redirects disabled")

    print("External-link safety rejected all unsafe offline fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
