from __future__ import annotations

from dataclasses import dataclass
import re

from playwright.sync_api import Page


KREAM_HOME = "https://kream.co.kr"


@dataclass
class RecordedSelectors:
    # Chrome Recorder에서 확인된 텍스트 기반 selector를 우선 사용한다.
    buy_or_bid_text: str = "즉시 구매 / 구매 입찰"
    buy_bid_text: str = "구매 입찰"
    bid_continue_text: str = "구매 입찰 계속"
    warehouse_text: str = "창고보관"
    thirty_days_text: str = "30일"
    desired_price_placeholder: str = "희망가 입력"


SEL = RecordedSelectors()


def parse_won(text: str) -> int | None:
    digits = re.sub(r"[^0-9]", "", text or "")
    return int(digits) if digits else None


def goto_product(page: Page, product_id: str | int) -> None:
    page.goto(f"{KREAM_HOME}/products/{product_id}", wait_until="domcontentloaded")


def open_buy_sheet(page: Page) -> None:
    # 녹화본에서 구매 버튼은 상품 상세의 두 번째 주요 버튼이었다.
    # 텍스트가 노출되는 경우 텍스트를 우선 사용하고, 그렇지 않으면 기존 클래스 기반 fallback.
    try:
        page.get_by_text("구매", exact=True).first.click(timeout=2500)
    except Exception:
        page.locator("div.layout-list-horizontal-not-equal button.pc\\:w-fill").nth(1).click()


def choose_size_by_text(page: Page, size: str) -> None:
    # size sheet 안에서 정확한 size 텍스트를 선택.
    page.get_by_text(size, exact=True).first.click()


def continue_to_buy_bid(page: Page) -> None:
    page.get_by_text(SEL.buy_or_bid_text, exact=False).click()
    page.get_by_role("link", name=SEL.buy_bid_text).click()


def fill_bid_form(page: Page, bid_price: int) -> None:
    page.get_by_role("link", name=SEL.buy_bid_text).click()
    page.get_by_label(SEL.desired_price_placeholder).fill(str(bid_price))
    page.get_by_text(SEL.thirty_days_text, exact=True).click()


def continue_to_storage(page: Page) -> None:
    page.get_by_role("button", name=SEL.bid_continue_text).click()
    page.get_by_text(SEL.warehouse_text, exact=True).click()


def stop_before_final_submit(page: Page) -> None:
    # 의도적으로 최종 결제/입찰 제출은 자동 클릭하지 않는다.
    print("DRY RUN: 창고보관 선택까지 완료. 최종 제출 전 중지.")
