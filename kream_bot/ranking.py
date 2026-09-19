from __future__ import annotations

import re

from playwright.sync_api import Page

KREAM_HOME = "https://kream.co.kr"


def open_ranking(page: Page) -> None:
    page.goto(KREAM_HOME, wait_until="domcontentloaded")
    page.get_by_text("랭킹", exact=True).first.click()
    page.wait_for_timeout(700)


def collect_product_urls(page: Page, max_products: int = 20) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()

    for _ in range(10):
        hrefs = page.locator('a[href*="/products/"]').evaluate_all(
            "(els) => els.map((e) => e.getAttribute('href')).filter(Boolean)"
        )

        for href in hrefs:
            match = re.search(r"/products/(\d+)", href)
            if not match:
                continue
            url = f"{KREAM_HOME}/products/{match.group(1)}"
            if url in seen:
                continue
            seen.add(url)
            urls.append(url)
            if len(urls) >= max_products:
                return urls

        page.mouse.wheel(0, 1100)
        page.wait_for_timeout(500)

    return urls[:max_products]
