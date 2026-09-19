from __future__ import annotations

import argparse

from kream_bot.browser import close_browser, open_browser, save_login
from kream_bot.ranking import collect_product_urls, open_ranking
from kream_bot.reporting import append_result, finish_report, save_error_screenshot, start_report
from kream_bot.scanner import scan_product_sizes


def parse_args():
    parser = argparse.ArgumentParser(description="KREAM ranking scanner - DRY RUN")
    parser.add_argument("--max-products", type=int, default=100)
    return parser.parse_args()


def main():
    args = parse_args()
    run_dir, result_file = start_report()
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

        append_result(result_file, {
            "type": "run_start",
            "product_count": len(product_urls),
            "dry_run": True,
        })

        for index, product_url in enumerate(product_urls, start=1):
            try:
                result = scan_product_sizes(page, product_url)
                sizes = ", ".join(result.sizes) if result.sizes else "(not detected)"
                print(f"[{index}/{len(product_urls)}] {product_url}")
                print(f"  sizes: {sizes}")

                append_result(result_file, {
                    "type": "product",
                    "index": index,
                    "product_url": product_url,
                    "sizes": result.sizes,
                    "status": "ok" if result.sizes else "not_detected",
                })
            except Exception as exc:
                print(f"[{index}/{len(product_urls)}] {product_url}")
                print(f"  error: {exc}")

                screenshot = save_error_screenshot(page, run_dir, index)
                append_result(result_file, {
                    "type": "product",
                    "index": index,
                    "product_url": product_url,
                    "status": "error",
                    "error": str(exc),
                    "screenshot": screenshot,
                })

        zip_path = finish_report(run_dir)

        print()
        print("DRY RUN finished. No purchase or bid was submitted.")
        print(f"TEST RESULT ZIP: {zip_path.resolve()}")
        print("Send this ZIP file back for review.")
        input("Press Enter to close the browser: ")
    finally:
        close_browser(pw, browser)


if __name__ == "__main__":
    main()
