from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import shutil

REPORT_DIR = Path("test_results")


def start_report() -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = REPORT_DIR / f"run_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir, run_dir / "result.jsonl"


def append_result(result_file: Path, payload: dict) -> None:
    with result_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def save_error_screenshot(page, run_dir: Path, index: int) -> str | None:
    path = run_dir / f"error_{index:03d}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
        return path.name
    except Exception:
        return None


def finish_report(run_dir: Path) -> Path:
    zip_path = shutil.make_archive(str(run_dir), "zip", root_dir=run_dir)
    return Path(zip_path)
