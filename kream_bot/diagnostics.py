from __future__ import annotations

from pathlib import Path
from datetime import datetime

from playwright.sync_api import Page


LOG_DIR = Path("logs")


def save_page_diagnostics(page: Page, label: str) -> tuple[Path, Path]:
    """
    Save a screenshot and visible page text for debugging selector changes.
    This does not submit any transaction.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_label = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in label)

    screenshot_path = LOG_DIR / f"{stamp}_{safe_label}.png"
    text_path = LOG_DIR / f"{stamp}_{safe_label}.txt"

    page.screenshot(path=str(screenshot_path), full_page=True)
    text_path.write_text(page.locator("body").inner_text(), encoding="utf-8")

    return screenshot_path, text_path
