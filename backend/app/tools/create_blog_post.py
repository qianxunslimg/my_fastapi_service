from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
import sys

import yaml

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.config import get_time_zone, settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new blog post scaffold.")
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument("--date", default="", help="Publish date in YYYY-MM-DD, defaults to today")
    parser.add_argument("--category", action="append", default=[], help="Category, can be repeated")
    parser.add_argument("--tag", action="append", default=[], help="Tag, can be repeated")
    parser.add_argument("--top", type=int, default=0, help="Pinned sort weight, defaults to 0")
    return parser.parse_args()


def build_storage_dir_name(title: str) -> str:
    raw = str(title or "").strip()
    normalized = "".join("-" if ch in '<>:"/\\\\|?*' or ord(ch) < 32 else ch for ch in raw)
    normalized = re.sub(r"\s+", " ", normalized).strip(" .-")
    if normalized:
        return normalized
    now = datetime.now(tz=get_time_zone())
    return now.strftime("post-%Y%m%d-%H%M%S")


def build_metadata(
    title: str,
    storage_dir_name: str,
    publish_at: datetime,
    categories: list[str],
    tags: list[str],
    top: int,
) -> dict[str, object]:
    metadata: dict[str, object] = {
        "date": publish_at.isoformat(),
    }
    if storage_dir_name != title.strip():
        metadata["title"] = title.strip()
    if categories:
        metadata["categories"] = categories
    if tags:
        metadata["tags"] = tags
    if top:
        metadata["top"] = top
    return metadata


def main() -> None:
    args = parse_args()
    now = datetime.now(tz=get_time_zone())
    publish_date = args.date.strip() or now.strftime("%Y-%m-%d")
    date_part = datetime.strptime(publish_date, "%Y-%m-%d")
    publish_at = get_time_zone().localize(
        datetime(
            year=date_part.year,
            month=date_part.month,
            day=date_part.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
            microsecond=now.microsecond,
        )
    )
    storage_dir_name = build_storage_dir_name(args.title)

    target_dir = Path(settings.BLOG_CONTENT_DIR) / date_part.strftime("%Y") / storage_dir_name
    assets_dir = target_dir / "assets"
    index_path = target_dir / "index.md"

    target_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    if index_path.exists():
        raise SystemExit(f"post already exists: {index_path}")

    metadata = build_metadata(
        title=args.title,
        storage_dir_name=storage_dir_name,
        publish_at=publish_at,
        categories=args.category,
        tags=args.tag,
        top=args.top,
    )
    front_matter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).strip()
    body = "\n".join(
        [
            "---",
            front_matter,
            "---",
            "",
            "> 摘要待补充",
            "",
            "## 开始写",
            "",
            "插图统一放在当前文章目录的 `assets/` 下，然后在正文里直接这样引用：",
            "",
            "![示例图片](./assets/example.png)",
            "",
        ]
    )
    index_path.write_text(body, encoding="utf-8")
    print(index_path)


if __name__ == "__main__":
    main()
