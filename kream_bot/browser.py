from __future__ import annotations

from pathlib import Path

from playwright.sync_api import BrowserContext, Page, sync_playwright


AUTH_FILE = Path("auth.json")


def open_browser(headless: bool = False):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)

    context_kwargs = {}
    if AUTH_FILE.exists():
        context_kwargs["storage_state"] = str(AUTH_FILE)

    context = browser.new_context(**context_kwargs)
    page = context.new_page()
    return playwright, browser, context, page


def save_login(context: BrowserContext) -> None:
    context.storage_state(path=str(AUTH_FILE))


def close_browser(playwright, browser) -> None:
    browser.close()
    playwright.stop()
