from __future__ import annotations

from dataclasses import dataclass
from playwright.sync_api import Page
from .flow import open_buy_sheet


@dataclass(frozen=True)
class ProductScan:
    product_url: str
    sizes: list[str]


def _read_size_tiles(page: Page) -> list[str]:
    """
    KREAM size picker is divided into tiles.
    Read the label from every visible tile so this works for shoes,
    clothing (S/M/L/XL), and other category-specific sizes.
    """
    tiles = page.locator("#teleports div.layout-grid-equal > div")
    sizes: list[str] = []
    seen: set[str] = set()

    for i in range(tiles.count()):
        tile = tiles.nth(i)
        if not tile.is_visible():
            continue

        # In the recorded KREAM UI, each tile contains size text and price text.
        # Prefer the first paragraph as the size label.
        paragraphs = tile.locator("p")
        if paragraphs.count():
            label = paragraphs.first.inner_text().strip()
        else:
            label = tile.inner_text().strip().splitlines()[0] if tile.inner_text().strip() else ""

        if not label or label in seen:
            continue

        seen.add(label)
        sizes.append(label)

    return sizes


def scan_product_sizes(page: Page, product_url: str) -> ProductScan:
    page.goto(product_url, wait_until="domcontentloaded")
    page.wait_for_timeout(700)
    open_buy_sheet(page)
    page.wait_for_timeout(400)

    sizes = _read_size_tiles(page)

    close_button = page.locator("div.bottom-sheet__close").last
    if close_button.count():
        try:
            close_button.click(timeout=1200)
        except Exception:
            pass

    return ProductScan(product_url=product_url, sizes=sizes)
