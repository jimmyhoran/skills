---
name: search-discovery
description: Prepare a new, changed, moved, or deleted website URL for discovery by search engines and AI answer engines. Use when the user asks to get a site or page indexed, request a recrawl or refetch, submit a URL to Brave, Google, or Bing, set up IndexNow, update or validate a sitemap, diagnose a page missing from search, or launch a newly published website. Check indexability and sitemap integrity before acting, follow each engine's current official discovery or submission guidance, and report submissions as requests rather than guaranteed indexing.
license: MIT
compatibility: Requires network access. Submission steps may require an authorized Google Search Console or Bing Webmaster Tools account and permission to update the target site's sitemap, robots.txt, or IndexNow key.
metadata:
  author: Jimmy Horan
  last-reviewed: "2026-07-22"
---

# Search Discovery

Make a page easy for search engines to find and recrawl. Submission is the final nudge, not a substitute for a crawlable, canonical, internally linked page.

**Freshness:** Engine routes and crawler policies were last reviewed on 2026-07-22. Re-check the linked first-party documentation at execution time because product flows, quotas, endpoints, and crawler behavior change.

## Determine the change set

Classify the request before making changes or submitting anything:

- **New site or launch:** homepage plus a small set of important, representative pages. Make sure the site can be reached without login or geographic/IP restrictions.
- **New page or material update:** the canonical URL of each changed page.
- **Migration, redirect, or deletion:** the old URL and its intended replacement or terminal status. Do not submit a redirect as though it were the page to index.
- **Many changed URLs:** submit a correct sitemap and use an automated notification mechanism where available; do not manually submit a large URL list.

Ask for the production domain, target URLs, and which webmaster accounts the user controls when they are not discoverable from the repository or prior context. Do not add verification tokens, change production configuration, or submit authenticated forms without authorization.

## Establish indexability first

For every priority URL, inspect the live production response, not only the local build. Confirm:

1. It returns a stable `200` response and loads without authentication.
2. It is not blocked by `robots.txt`, an `X-Robots-Tag`, or a page-level `noindex` directive.
3. Its canonical URL is absolute, intended, and self-referential (unless the page intentionally canonicalizes elsewhere).
4. It is reachable from normal HTML links on the site, ideally from the homepage or a section hub.
5. Its rendered content is useful and materially different from canonical alternatives; submitting a thin, duplicate, error, or redirect URL will not fix its indexability.

For a missing or stale result, inspect the engine's URL-level report before re-submitting. Diagnose the actual reason: blocked crawling, `noindex`, canonical selection, redirect, server failure, duplicate content, or quality exclusion. Fix that cause before requesting another crawl.

## Keep the sitemap truthful

Treat sitemap work as part of this skill, not as a separate workflow.

1. Find the sitemap through `robots.txt`, the CMS/framework configuration, or common locations such as `/sitemap.xml`.
2. Confirm it is publicly fetchable and syntactically valid, and that it lists the canonical production URLs only.
3. Check a representative sample for `200` responses, self-canonicals, and indexability. Exclude redirects, `4xx`/`5xx` pages, `noindex` pages, staging URLs, and duplicate parameter variants.
4. Add new canonical URLs; remove deleted URLs; replace moved URLs with their final destinations.
5. Set `<lastmod>` only when the page changed materially, using the actual modification date. Do not rewrite every timestamp merely to provoke crawls.
6. Ensure `robots.txt` advertises the sitemap and submit or refresh it in Google Search Console and Bing Webmaster Tools when the user owns those properties.

For a handful of high-priority updates, pair sitemap maintenance with individual requests. For a site-wide release, sitemap integrity is the primary action.

## Notify engines through their current official routes

Check the official documentation at execution time. Product flows, endpoints, quotas, and supported engines can change.

| Service | Preferred action | Notes |
| --- | --- | --- |
| Brave Search | Open [Submit URL](https://search.brave.com/submit-url) and submit the canonical URL. | Manual discovery request; record that it was submitted. |
| Google Search | Follow Google's [recrawl guidance](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl): inspect the canonical URL in the owned Search Console property, run **Test live URL** where appropriate, then choose **Request indexing**. Submit the sitemap for many URLs. | This is a request with a quota, not an indexing guarantee. Do not use Google's Indexing API for ordinary web pages. |
| Bing | Prefer [IndexNow](https://www.indexnow.org/documentation) for URLs published, updated, moved, or deleted. Use [Bing Webmaster Tools' URL Submission](https://www.bing.com/webmasters/help/url-submission-62f2860b) only for a small fallback set. | Verify domain ownership/key placement before sending URLs. Send only changed URLs. |
| ChatGPT Search | Follow OpenAI's [publisher guidance](https://help.openai.com/en/articles/12627856-publishers-and-developers-faq) and allow `OAI-SearchBot` where inclusion is intended. | There is no manual indexing request in the cited guidance; do not invent one or conflate `OAI-SearchBot` with `GPTBot`. |
| DuckDuckGo | Do not present Bing or IndexNow submission as a DuckDuckGo submission. Check DuckDuckGo's current [source](https://duckduckgo.com/duckduckgo-help-pages/results/sources) and [crawler](https://duckduckgo.com/duckduckgo-help-pages/results/duckduckbot) guidance before claiming a direct route exists. | Maintain ordinary crawlability and sitemap accuracy; treat Bing as one source, not a DuckDuckGo submission endpoint. |
| Perplexity | Do not invent a submit or refetch endpoint. Check Perplexity's current [crawler policy](https://www.perplexity.ai/help-center/en/articles/10354969-how-does-perplexity-follow-robots-txt) before taking action. | Make public pages crawlable and use normal search-discovery signals. |

Never say a page "will come up in search" after submission. Say it was requested or notified. Indexing and ranking remain each service's decision.

## Use IndexNow for repeatable publishing

Recommend IndexNow when the site has a custom publishing pipeline, CMS integration, CDN integration, or frequent changes.

1. Generate an IndexNow key.
2. Host the plain-text key file at the verified location on the production host.
3. Send a single URL or a bounded batch only when URLs are added, materially updated, moved, or deleted.
4. Inspect submission, crawl, and indexing status in Bing Webmaster Tools.

Do not backfill the entire historical site merely because IndexNow was added today. Do not send unchanged URLs repeatedly. If a CMS, CDN, or host already emits IndexNow notifications, verify that integration before adding another sender.

## Verify and report honestly

After a request, capture the URL, engine, method, time, and any confirmation or error. Then state the appropriate follow-up:

- **Immediate:** verify the live response, canonical, robots directives, and sitemap entry.
- **Later:** use Search Console and Bing Webmaster Tools to inspect crawl/index status; use site queries only as a rough public signal.
- **If still absent:** return to the indexability diagnosis rather than repeatedly submitting the same URL.

End with a compact table: **URL · change type · sitemap status · request/notification sent · evidence · next check**. Separate completed actions from prerequisites the user must complete, such as property verification or an unavailable authenticated account.
