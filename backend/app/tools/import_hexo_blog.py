from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

import yaml


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core.config import get_time_zone, settings


FRONT_MATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
MARKDOWN_IMAGE_PATTERN = re.compile(r"(!\[[^\]]*\]\()([^)]+?)(\))")
HTML_IMAGE_PATTERN = re.compile(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])', re.IGNORECASE)
HTML_HREF_PATTERN = re.compile(r'(<a\b[^>]*?\bhref=["\'])([^"\']+)(["\'])', re.IGNORECASE)
TITLE_SPLIT_PATTERN = re.compile(r"[/／|｜]")
REMOTE_IMAGE_HOSTS = {
    "qianxunslimg.oss-cn-beijing.aliyuncs.com",
    "shuaidi-picture-1257337429.cos.ap-guangzhou.myqcloud.com",
}
IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".webp",
    ".svg",
    ".avif",
}
CONTENT_TYPE_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
    "image/svg+xml": ".svg",
    "image/avif": ".avif",
}
USER_AGENT = "Mozilla/5.0 (Codex Blog Importer)"
ENCRYPTED_SUMMARY = "Here's something encrypted, password is required to continue reading."


@dataclass(frozen=True)
class ExistingPost:
    index_path: Path
    metadata: dict[str, Any]
    title_key: str
    date_key: str
    slug: str
    legacy_path: str


@dataclass(frozen=True)
class GeneratedPost:
    title_key: str
    date_key: str
    slug: str
    legacy_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Overlay real Hexo markdown posts onto the imported blog content."
    )
    parser.add_argument(
        "source_root",
        help="Hexo project root or source/_posts directory",
    )
    parser.add_argument(
        "--output-root",
        default=settings.BLOG_CONTENT_DIR,
        help="Target blog posts directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would change",
    )
    return parser.parse_args()


def resolve_source_posts_root(source_root: Path) -> Path:
    candidate = (source_root / "source" / "_posts").resolve()
    if candidate.is_dir():
        return candidate
    direct = source_root.resolve()
    if direct.is_dir():
        return direct
    raise FileNotFoundError(f"source posts root not found: {source_root}")


def resolve_public_root(source_root: Path) -> Path | None:
    candidate = (source_root / "public").resolve()
    if candidate.is_dir():
        return candidate
    parent_candidate = (source_root.parent / "public").resolve()
    if parent_candidate.is_dir():
        return parent_candidate
    return None


def load_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        raise ValueError(f"missing front matter: {path}")
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"invalid front matter metadata: {path}")
    body = match.group(2).strip()
    return metadata, body


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", "", value).strip().lower()


def title_match_keys(value: str) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []

    keys: list[str] = []
    seen: set[str] = set()

    def add(candidate: str) -> None:
        key = normalize_title(candidate)
        if key and key not in seen:
            seen.add(key)
            keys.append(key)

    add(text)
    parts = [part.strip() for part in TITLE_SPLIT_PATTERN.split(text) if part.strip()]
    if len(parts) > 1:
        for end in range(len(parts) - 1, 1, -1):
            add("/".join(parts[:end]))
    return keys


def normalize_datetime_string(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError("missing datetime value")

    normalized = text.replace("Z", "+00:00")
    parsed: datetime
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")

    if parsed.tzinfo is None:
        parsed = get_time_zone().localize(parsed)
    else:
        parsed = parsed.astimezone(get_time_zone())
    return parsed.isoformat()


def normalize_date_key(value: Any) -> str:
    if not value:
        return ""
    return normalize_datetime_string(value)[:10]


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    if normalized:
        return normalized
    return "post"


def build_storage_dir_name(title: str, slug: str) -> str:
    raw = str(title or "").strip()
    normalized = "".join("-" if ch in '<>:"/\\\\|?*' or ord(ch) < 32 else ch for ch in raw)
    normalized = re.sub(r"\s+", " ", normalized).strip(" .-")
    if normalized:
        return normalized
    return slug


def normalize_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = [str(item) for item in value]
    else:
        items = [str(value)]

    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def normalize_int(value: Any) -> int:
    if value is None:
        return 0
    text = str(value).strip()
    if not text:
        return 0
    try:
        return int(text)
    except ValueError:
        return 0


def merge_str_lists(*values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for items in values:
        for item in items:
            text = item.strip()
            if not text or text in seen:
                continue
            seen.add(text)
            merged.append(text)
    return merged


def derive_legacy_path(date_value: Any, slug: str) -> str:
    if not slug:
        return ""
    date_iso = normalize_datetime_string(date_value)
    return f"/{date_iso[:10].replace('-', '/')}/{slug}/"


def build_existing_index(
    output_root: Path,
) -> tuple[dict[str, list[ExistingPost]], dict[str, ExistingPost], dict[str, ExistingPost]]:
    by_title: dict[str, list[ExistingPost]] = {}
    by_slug: dict[str, ExistingPost] = {}
    by_legacy_path: dict[str, ExistingPost] = {}
    for index_path in sorted(output_root.rglob("index.md")):
        if not index_path.is_file():
            continue
        try:
            metadata, _ = load_front_matter(index_path)
        except Exception:
            continue

        title = str(metadata.get("title") or index_path.parent.name).strip()
        if not title:
            continue
        key = normalize_title(title)
        slug = str(metadata.get("slug") or "").strip()
        legacy_path = str(metadata.get("legacy_path") or "").strip()
        if not legacy_path:
            legacy_path = derive_legacy_path(metadata.get("date"), slug)
        existing = ExistingPost(
            index_path=index_path,
            metadata=metadata,
            title_key=key,
            date_key=normalize_date_key(metadata.get("date")),
            slug=slug,
            legacy_path=legacy_path,
        )
        by_title.setdefault(key, []).append(existing)
        if existing.slug:
            by_slug.setdefault(existing.slug, existing)
        if existing.legacy_path:
            by_legacy_path.setdefault(existing.legacy_path, existing)
    return by_title, by_slug, by_legacy_path


def build_generated_index(public_root: Path | None) -> dict[str, list[GeneratedPost]]:
    if public_root is None:
        return {}

    by_title: dict[str, list[GeneratedPost]] = {}
    for index_path in sorted(public_root.rglob("index.html")):
        try:
            relative_path = index_path.relative_to(public_root).as_posix()
        except ValueError:
            continue
        match = re.match(r"^(\d{4})/(\d{2})/(\d{2})/([^/]+)/index\.html$", relative_path)
        if not match:
            continue

        html = index_path.read_text(encoding="utf-8", errors="ignore")
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if title_match is None:
            title_match = re.search(r"<h1[^>]*class=\"post-title\"[^>]*>(.*?)</h1>", html)
        if title_match is None:
            continue

        title_key = normalize_title(title_match.group(1).strip())
        generated = GeneratedPost(
            title_key=title_key,
            date_key=f"{match.group(1)}-{match.group(2)}-{match.group(3)}",
            slug=match.group(4),
            legacy_path=f"/{match.group(1)}/{match.group(2)}/{match.group(3)}/{match.group(4)}/",
        )
        by_title.setdefault(title_key, []).append(generated)
    return by_title


def select_existing_post(
    source_metadata: dict[str, Any], existing_index: dict[str, list[ExistingPost]]
) -> ExistingPost | None:
    title = str(source_metadata.get("title") or "").strip()
    if not title:
        return None

    candidates: list[ExistingPost] = []
    for key in title_match_keys(title):
        candidates = existing_index.get(key, [])
        if candidates:
            break
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    date_key = normalize_date_key(source_metadata.get("date"))
    if date_key:
        same_day = [post for post in candidates if post.date_key == date_key]
        if len(same_day) == 1:
            return same_day[0]
        if same_day:
            candidates = same_day

    candidates = sorted(candidates, key=lambda item: str(item.index_path))
    return candidates[0]


def select_generated_post(
    source_metadata: dict[str, Any], generated_index: dict[str, list[GeneratedPost]]
) -> GeneratedPost | None:
    title = str(source_metadata.get("title") or "").strip()
    if not title:
        return None

    candidates: list[GeneratedPost] = []
    for key in title_match_keys(title):
        candidates = generated_index.get(key, [])
        if candidates:
            break
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    date_key = normalize_date_key(source_metadata.get("date"))
    if date_key:
        same_day = [post for post in candidates if post.date_key == date_key]
        if len(same_day) == 1:
            return same_day[0]
        if same_day:
            candidates = same_day

    candidates = sorted(candidates, key=lambda item: (item.date_key, item.slug))
    return candidates[0]


def derive_new_index_path(
    output_root: Path,
    source_metadata: dict[str, Any],
    existing_metadata: dict[str, Any] | None,
    generated_post: GeneratedPost | None,
) -> Path:
    title = str((source_metadata or {}).get("title") or (existing_metadata or {}).get("title") or "").strip()
    slug = str((existing_metadata or {}).get("slug") or "").strip()
    if not slug and generated_post is not None:
        slug = generated_post.slug
    if not slug:
        slug = slugify(str(source_metadata.get("title") or "post"))
    storage_dir_name = build_storage_dir_name(title, slug)
    year = normalize_datetime_string(
        (existing_metadata or {}).get("date") or source_metadata.get("date")
    )[:4]
    return output_root / year / storage_dir_name / "index.md"


def ensure_unique_index_path(index_path: Path, slug: str, reserved_paths: set[Path]) -> Path:
    if index_path not in reserved_paths and not index_path.exists():
        return index_path

    base_dir = index_path.parent
    parent_dir = base_dir.parent
    candidate = parent_dir / f"{base_dir.name} - {slug}" / "index.md"
    if candidate not in reserved_paths and not candidate.exists():
        return candidate

    counter = 2
    while True:
        candidate = parent_dir / f"{base_dir.name} - {slug}-{counter}" / "index.md"
        if candidate not in reserved_paths and not candidate.exists():
            return candidate
        counter += 1


def strip_query_fragment(raw_url: str) -> str:
    return raw_url.split("#", 1)[0].split("?", 1)[0]


def looks_like_image_url(raw_url: str) -> bool:
    cleaned = strip_query_fragment(raw_url).strip()
    if not cleaned or cleaned.startswith("data:"):
        return False
    parsed = urlparse(cleaned)
    if parsed.scheme in {"http", "https"} and parsed.netloc.lower() in REMOTE_IMAGE_HOSTS:
        return True
    return Path(unquote(parsed.path)).suffix.lower() in IMAGE_EXTENSIONS


def safe_asset_name(raw_url: str, content_type: str | None = None) -> str:
    parsed = urlparse(raw_url)
    raw_name = Path(unquote(parsed.path)).name
    stem = Path(raw_name).stem
    suffix = Path(raw_name).suffix.lower()

    if not suffix and content_type:
        suffix = CONTENT_TYPE_EXTENSIONS.get(content_type.lower(), "")
    if suffix not in IMAGE_EXTENSIONS:
        suffix = suffix or ".bin"

    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-")
    if not safe_stem:
        safe_stem = "asset"
    return f"{safe_stem}{suffix}"


def unique_destination(directory: Path, filename: str) -> Path:
    candidate = directory / filename
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        next_candidate = directory / f"{stem}-{counter}{suffix}"
        if not next_candidate.exists():
            return next_candidate
        counter += 1


def write_missing_asset_placeholder(destination: Path, label: str) -> None:
    safe_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">
<rect width="640" height="360" fill="#f3f4f6"/>
<rect x="24" y="24" width="592" height="312" rx="16" fill="#ffffff" stroke="#d1d5db" stroke-width="2"/>
<text x="320" y="160" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#111827">Missing Asset</text>
<text x="320" y="196" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#6b7280">{safe_label}</text>
</svg>
"""
    destination.write_text(svg, encoding="utf-8")


def download_remote_asset(raw_url: str, assets_dir: Path, dry_run: bool) -> str:
    request = Request(raw_url, headers={"User-Agent": USER_AGENT})
    if dry_run:
        filename = safe_asset_name(raw_url, "image/png")
        destination = unique_destination(assets_dir, filename)
        return f"./assets/{destination.name}"

    try:
        with urlopen(request, timeout=20) as response:
            data = response.read()
            content_type = response.headers.get_content_type()
    except (HTTPError, URLError, TimeoutError, ValueError):
        destination = unique_destination(assets_dir, safe_asset_name(raw_url, "image/svg+xml"))
        if destination.suffix.lower() != ".svg":
            destination = destination.with_suffix(".svg")
        if not dry_run:
            write_missing_asset_placeholder(
                destination,
                Path(strip_query_fragment(raw_url)).name or raw_url,
            )
        return f"./assets/{destination.name}"

    destination = unique_destination(assets_dir, safe_asset_name(raw_url, content_type))
    destination.write_bytes(data)
    return f"./assets/{destination.name}"


def resolve_local_asset_path(source_post_path: Path, raw_url: str) -> Path | None:
    decoded = unquote(strip_query_fragment(raw_url))
    if not decoded or decoded.startswith("/"):
        return None

    direct = (source_post_path.parent / decoded).resolve()
    if direct.exists() and direct.is_file():
        return direct

    asset_folder = source_post_path.with_suffix("")
    nested = (asset_folder / decoded).resolve()
    if nested.exists() and nested.is_file():
        return nested
    return None


def copy_local_asset(asset_path: Path, assets_dir: Path, dry_run: bool) -> str:
    destination = unique_destination(assets_dir, safe_asset_name(asset_path.as_posix()))
    if not dry_run:
        shutil.copy2(asset_path, destination)
    return f"./assets/{destination.name}"


def localize_asset(
    raw_url: str,
    source_post_path: Path,
    assets_dir: Path,
    cache: dict[str, str],
    dry_run: bool,
) -> str:
    normalized = raw_url.strip()
    if not normalized or normalized.startswith(("data:", "#")):
        return raw_url

    if normalized in cache:
        return cache[normalized]

    parsed = urlparse(normalized)
    if parsed.scheme in {"http", "https"} and looks_like_image_url(normalized):
        localized = download_remote_asset(normalized, assets_dir, dry_run)
        cache[normalized] = localized
        return localized

    if not parsed.scheme:
        local_path = resolve_local_asset_path(source_post_path, normalized)
        if local_path is not None:
            localized = copy_local_asset(local_path, assets_dir, dry_run)
            cache[normalized] = localized
            return localized
        if looks_like_image_url(normalized):
            destination = unique_destination(assets_dir, safe_asset_name(normalized, "image/svg+xml"))
            if destination.suffix.lower() != ".svg":
                destination = destination.with_suffix(".svg")
            if not dry_run:
                write_missing_asset_placeholder(
                    destination,
                    Path(strip_query_fragment(normalized)).name or normalized,
                )
            localized = f"./assets/{destination.name}"
            cache[normalized] = localized
            return localized

    return raw_url


def rewrite_html_assets(
    body: str,
    source_post_path: Path,
    assets_dir: Path,
    cache: dict[str, str],
    dry_run: bool,
) -> str:
    def replace_img(match: re.Match[str]) -> str:
        localized = localize_asset(match.group(2), source_post_path, assets_dir, cache, dry_run)
        return f"{match.group(1)}{localized}{match.group(3)}"

    def replace_href(match: re.Match[str]) -> str:
        href = match.group(2)
        if not looks_like_image_url(href):
            return match.group(0)
        localized = localize_asset(href, source_post_path, assets_dir, cache, dry_run)
        return f"{match.group(1)}{localized}{match.group(3)}"

    body = HTML_IMAGE_PATTERN.sub(replace_img, body)
    body = HTML_HREF_PATTERN.sub(replace_href, body)
    return body


def rewrite_markdown_images(
    body: str,
    source_post_path: Path,
    assets_dir: Path,
    cache: dict[str, str],
    dry_run: bool,
) -> str:
    def replace_image(match: re.Match[str]) -> str:
        localized = localize_asset(match.group(2), source_post_path, assets_dir, cache, dry_run)
        return f"{match.group(1)}{localized}{match.group(3)}"

    return MARKDOWN_IMAGE_PATTERN.sub(replace_image, body)


def summarize_markdown(body: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", body)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[(.*?)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[>*_~\-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 180:
        return text[:180].rstrip() + "..."
    return text


def build_metadata(
    source_metadata: dict[str, Any],
    existing_metadata: dict[str, Any] | None,
    generated_post: GeneratedPost | None,
    storage_dir_name: str,
) -> dict[str, Any]:
    existing = existing_metadata or {}
    title = str(source_metadata.get("title") or existing.get("title") or "").strip()
    if not title:
        raise ValueError("missing post title")

    source_tags = normalize_str_list(source_metadata.get("tags"))
    source_categories = normalize_str_list(source_metadata.get("categories"))
    existing_tags = normalize_str_list(existing.get("tags"))
    existing_categories = normalize_str_list(existing.get("categories"))

    slug = str(existing.get("slug") or "").strip()
    if not slug and generated_post is not None:
        slug = generated_post.slug
    if not slug:
        slug = slugify(title)
    date_value = existing.get("date") or source_metadata.get("date")
    updated_value = existing.get("updated") or source_metadata.get("updated") or date_value
    date_iso = normalize_datetime_string(date_value)
    updated_iso = normalize_datetime_string(updated_value)

    hidden = bool(source_metadata.get("hidden") if "hidden" in source_metadata else existing.get("hidden"))
    password = str(source_metadata.get("password") or existing.get("password") or "").strip()
    top = normalize_int(source_metadata.get("top") if "top" in source_metadata else existing.get("top"))

    metadata: dict[str, Any] = {
        "date": date_iso,
    }
    if storage_dir_name != title:
        metadata["title"] = title
    if updated_iso != date_iso:
        metadata["updated"] = updated_iso
    merged_categories = source_categories or existing_categories
    merged_tags = source_tags or existing_tags
    if merged_categories:
        metadata["categories"] = merged_categories
    if merged_tags:
        metadata["tags"] = merged_tags
    if hidden:
        metadata["hidden"] = hidden
    if password:
        metadata["password"] = password
    if top:
        metadata["top"] = top
    return metadata


def write_post(index_path: Path, metadata: dict[str, Any], body: str, dry_run: bool) -> None:
    front_matter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).strip()
    content = "\n".join(
        [
            "---",
            front_matter,
            "---",
            "",
            body.strip(),
            "",
        ]
    )

    if dry_run:
        return

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    source_posts_root = resolve_source_posts_root(Path(args.source_root))
    public_root = resolve_public_root(Path(args.source_root))
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    existing_index, existing_by_slug, existing_by_legacy_path = build_existing_index(output_root)
    generated_index = build_generated_index(public_root)
    updated_count = 0
    created_count = 0
    unmatched_titles: list[str] = []
    skipped_sources: list[str] = []
    planned_index_paths: set[Path] = set()

    for source_post_path in sorted(source_posts_root.glob("*.md")):
        try:
            source_metadata, source_body = load_front_matter(source_post_path)
        except ValueError:
            skipped_sources.append(source_post_path.name)
            continue
        if bool(source_metadata.get("draft")):
            continue

        existing_post = select_existing_post(source_metadata, existing_index)
        generated_post = select_generated_post(source_metadata, generated_index)
        if existing_post is None and generated_post is not None:
            existing_post = existing_by_legacy_path.get(generated_post.legacy_path)
        if existing_post is None and generated_post is not None:
            existing_post = existing_by_slug.get(generated_post.slug)
        existing_metadata = existing_post.metadata if existing_post else None
        target_index_path = (
            existing_post.index_path
            if existing_post
            else derive_new_index_path(
                output_root,
                source_metadata,
                existing_metadata,
                generated_post,
            )
        )
        if existing_post is None:
            slug = str((existing_metadata or {}).get("slug") or "").strip()
            if not slug and generated_post is not None:
                slug = generated_post.slug
            if not slug:
                slug = slugify(str(source_metadata.get("title") or "post"))
            target_index_path = ensure_unique_index_path(target_index_path, slug, planned_index_paths)
        planned_index_paths.add(target_index_path)
        assets_dir = target_index_path.parent / "assets"
        if not args.dry_run:
            assets_dir.mkdir(parents=True, exist_ok=True)

        asset_cache: dict[str, str] = {}
        rewritten_body = rewrite_html_assets(
            source_body,
            source_post_path,
            assets_dir,
            asset_cache,
            args.dry_run,
        )
        rewritten_body = rewrite_markdown_images(
            rewritten_body,
            source_post_path,
            assets_dir,
            asset_cache,
            args.dry_run,
        )

        metadata = build_metadata(
            source_metadata,
            existing_metadata,
            generated_post,
            target_index_path.parent.name,
        )
        write_post(target_index_path, metadata, rewritten_body, args.dry_run)

        if existing_post:
            updated_count += 1
        else:
            created_count += 1
            unmatched_titles.append(metadata["title"])

    print(f"updated: {updated_count}")
    print(f"created: {created_count}")
    if unmatched_titles:
        print("created_titles:")
        for title in unmatched_titles:
            print(f"- {title}")
    if skipped_sources:
        print(f"skipped: {len(skipped_sources)}")


if __name__ == "__main__":
    main()
