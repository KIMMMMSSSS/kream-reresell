from __future__ import annotations

import argparse

from kream_bot.browser import close_browser, open_browser, save_login
from kream_bot.flow import continue_to_buy_bid, continue_to_storage, fill_bid_form, goto_product, open_buy_sheet, choose_size_by_text


def parse_args():
    p = argparse.ArgumentParser(description="KREAM 구매입찰 보조 자동화")
    p.add_argument("--product-id", required=True, help="KREAM 상품 ID")
    p.add_argument("--size", required=True, help="사이즈, 예: 240")
    p.add_argument("--bid-price", type=int, required=True, help="테스트용 구매입찰 희망가")
    return p.parse_args()


def main():
    args = parse_args()
    pw, browser, context, page = open_browser(headless=False)
    try:
        goto_product(page, args.product_id)
        input("KREAM 로그인 상태를 확인하세요. 준비되면 Enter: ")
        save_login(context)

        open_buy_sheet(page)
        choose_size_by_text(page, args.size)
        continue_to_buy_bid(page)
        fill_bid_form(page, args.bid_price)
        continue_to_storage(page)

        print("DRY RUN 완료: 최종 제출은 누르지 않았습니다.")
        input("브라우저를 확인한 뒤 Enter를 누르면 종료합니다: ")
    finally:
        close_browser(pw, browser)


if __name__ == "__main__":
    main()
