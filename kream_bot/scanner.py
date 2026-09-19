from __future__ import annotations

import re
from dataclasses import dataclass
from playwright.sync_api import Page
from .flow import open_buy_sheet

@dataclass(frozen=True)
class ProductScan:
    product_url: str
    sizes: list[str]

def _numeric_sizes(texts: list[str]) -> list[str]:
    values = set()
    for text in texts:
        value = (text or "").strip()
        if re.fullmatch(r"\d{3}", value):
            size = int(value)
            if 240 <= size <= 320:
                values.add(size)
    return [str(size) for size in sorted(values)]

def scan_product_sizes(page: Page, product_url: str) -> ProductScan:
    page.goto(product_url, wait_until="domcontentloaded")
    page.wait_for_timeout(700)
    open_buy_sheet(page)
    page.wait_for_timeout(400)
    texts = page.locator("#teleports p").all_inner_texts()
    sizes = _numeric_sizes(texts)
    close_button = page.locator("div.bottom-sheet__close").last
    if close_button.count():
        try:
            close_button.click(timeout=1200)
        except Exception:
            pass
    return ProductScan(product_url=product_url, sizes=sizes)
