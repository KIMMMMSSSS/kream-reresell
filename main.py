from __future__ import annotations

import argparse

from kream_bot.browser import close_browser, open_browser, save_login
from kream_bot.ranking import collect_product_urls, open_ranking
from kream_bot.scanner import scan_product_sizes


def parse_args():
    parser = argparse.ArgumentParser(description="KREAM ranking scanner - DRY RUN")
    parser.add_argument("--max-products", type=int, default=100)
    return parser.parse_args()


def main():
    args = parse_args()
    pw, browser, context, page = open_browser(headless=False)

    try:
        open_ranking(page)

        print("KREAM ranking page opened.")
        print("Log in if needed, then choose the category you want in the browser.")
        input("When the category page is ready, press Enter here: ")

        save_login(context)
        product_urls = collect_product_urls(page, max_products=args.max_products)

        print(f"Found {len(product_urls)} product pages.")
        print("DRY RUN: this version only visits products and reads sizes.")

        for index, product_url in enumerate(product_urls, start=1):
            try:
                result = scan_product_sizes(page, product_url)
                sizes = ", ".join(result.sizes) if result.sizes else "(not detected)"
                print(f"[{index}/{len(product_urls)}] {product_url}")
                print(f"  sizes: {sizes}")
            except Exception as exc:
                print(f"[{index}/{len(product_urls)}] {product_url}")
                print(f"  error: {exc}")

        print("DRY RUN finished. No purchase or bid was submitted.")
        input("Press Enter to close the browser: ")
    finally:
        close_browser(pw, browser)


if __name__ == "__main__":
    main()
