from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from threading import RLock
from typing import Any, Iterable, Optional
from urllib.parse import quote, urlparse

import mistune
import yaml
from bs4 import BeautifulSoup

from core.config import get_time_zone, settings


POST_INDEX_NAME = "index.md"
FRONT_MATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
MARKDOWN_RENDERER = mistune.create_markdown(
    escape=False,
    plugins=["strikethrough", "table", "task_lists", "url"],
)
BLOG_LOCK = RLock()
BLOG_CACHE_SIGNATURE: tuple[tuple[str, int], ...] | None = None
BLOG_CACHE_DATA: "BlogCatalog | None" = None
OLD_SITE_HOST = "qianxunslimg.github.io"
ENCRYPTED_SUMMARY = "Here's something encrypted, password is required to continue reading."
ENCRYPTED_EXCERPT = "Hey, password is required here."
PASSWORD_PLACEHOLDER_HTML = (
    '<div class="blog-password-placeholder">'
    "<p>Password is required to view this article.</p>"
    "</div>"
)


@dataclass(frozen=True)
class BlogFacetItem:
    name: str
    count: int


@dataclass(frozen=True)
class BlogPostRecord:
    title: str
    storage_path: str
    post_path: str
    url_path: str
    published_at: str
    updated_at: Optional[str]
    summary: str
    excerpt: str
    categories: tuple[str, ...]
    tags: tuple[str, ...]
    cover_image: Optional[str]
    word_count: int
    reading_minutes: int
    top: int
    content_html: str
    password: str
    sort_key: datetime

    def _to_payload(self, password: str = "", include_content: bool = False) -> dict[str, Any]:
        password_required = bool(self.password)
        password_unlocked = not password_required or password == self.password
        locked = password_required and not password_unlocked

        return {
            "title": self.title,
            "post_path": self.post_path,
            "url_path": self.url_path,
            "published_at": self.published_at,
            "updated_at": self.updated_at,
            "summary": ENCRYPTED_SUMMARY if locked else self.summary,
            "excerpt": ENCRYPTED_EXCERPT if locked else self.excerpt,
            "categories": list(self.categories),
            "tags": list(self.tags),
            "cover_image": None if locked else self.cover_image,
            "word_count": 0 if locked else self.word_count,
            "reading_minutes": 1 if locked else self.reading_minutes,
            "top": self.top,
            "password_required": password_required,
            "password_unlocked": password_unlocked,
            **({"content_html": self.content_html if password_unlocked else ""} if include_content else {}),
        }

    def to_summary(self) -> dict[str, Any]:
        return self._to_payload()

    def to_detail(self, password: str = "") -> dict[str, Any]:
        return self._to_payload(password=password, include_content=True)


@dataclass(frozen=True)
class BlogCatalog:
    posts: tuple[BlogPostRecord, ...]
    tags: tuple[BlogFacetItem, ...]
    categories: tuple[BlogFacetItem, ...]
    post_map: dict[str, BlogPostRecord]


def _posts_root() -> Path:
    return Path(settings.BLOG_CONTENT_DIR).resolve()


def _normalize_datetime(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None

    normalized = text.replace("Z", "+00:00")
    parsed: datetime

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
            try:
                parsed = datetime.strptime(text, fmt)
                break
            except ValueError:
                continue
        else:
            raise

    if parsed.tzinfo is None:
        parsed = get_time_zone().localize(parsed)
    else:
        parsed = parsed.astimezone(get_time_zone())
    return parsed.isoformat()


def _load_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        raise ValueError("missing front matter")

    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise ValueError("invalid front matter metadata")
    body = match.group(2).strip()
    return metadata, body


def _normalize_str_list(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, Iterable):
        items = [str(item) for item in value if str(item).strip()]
    else:
        items = [str(value)]

    normalized: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = item.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return tuple(normalized)


def _normalize_int(value: Any) -> int:
    if value is None:
        return 0
    text = str(value).strip()
    if not text:
        return 0
    try:
        return int(text)
    except ValueError:
        return 0


def _build_content_signature() -> tuple[tuple[str, int], ...]:
    root = _posts_root()
    files = sorted(root.rglob(POST_INDEX_NAME))
    return tuple(
        (str(path.relative_to(root).as_posix()), path.stat().st_mtime_ns)
        for path in files
        if path.is_file()
    )


def _quote_path(path: str) -> str:
    return "/".join(quote(part) for part in PurePosixPath(path).parts)


def _is_relative_url(value: str) -> bool:
    if not value:
        return False
    if value.startswith(("#", "/", "//")):
        return False
    parsed = urlparse(value)
    return not parsed.scheme


def _build_asset_url(target_path: str) -> str:
    quoted = _quote_path(target_path)
    return f"{settings.API_PREFIX}/blog/assets/{quoted}"


def _rewrite_relative_url(storage_path: str, raw_url: str) -> str:
    resolved = PurePosixPath(storage_path, raw_url).as_posix()
    normalized = PurePosixPath(resolved).as_posix()
    return _build_asset_url(normalized)


def _rewrite_internal_link(href: str) -> str:
    text = href.strip()
    if not text or text.startswith(("#", "mailto:", "tel:")):
        return href

    parsed = urlparse(text)
    host = parsed.netloc.lower()
    path = parsed.path or ""

    if parsed.scheme in {"http", "https"} and host and host != OLD_SITE_HOST:
        return href

    target_path = path
    if target_path.startswith("/tags/"):
        encoded = target_path.removeprefix("/tags/").strip("/")
        return f"/blog/tags/{encoded}"
    if target_path.startswith("/categories/"):
        encoded = target_path.removeprefix("/categories/").strip("/")
        return f"/blog/categories/{encoded}"
    if re.match(r"^/\d{4}/\d{2}/\d{2}/[^/]+/?$", target_path):
        return "/blog" + target_path.rstrip("/")
    if target_path.startswith("/archives"):
        return "/blog"
    return href


def _rewrite_rendered_html(content_html: str, storage_path: str) -> str:
    soup = BeautifulSoup(content_html, "html.parser")

    for image in soup.select("img[src]"):
        src = image.get("src", "").strip()
        if not src:
            continue
        image.attrs.pop("srcset", None)
        image.attrs.pop("data-src", None)
        image.attrs.pop("data-srcset", None)
        image.attrs.pop("lazyload", None)
        if _is_relative_url(src):
            image["src"] = _rewrite_relative_url(storage_path, src)
            continue
        parsed = urlparse(src)
        if parsed.scheme in {"http", "https"} and parsed.netloc.lower() == OLD_SITE_HOST:
            image["src"] = _rewrite_internal_link(src)

    for link in soup.select("a[href]"):
        href = link.get("href", "").strip()
        if not href:
            continue
        if _is_relative_url(href):
            link["href"] = _rewrite_relative_url(storage_path, href)
            continue
        link["href"] = _rewrite_internal_link(href)

    return str(soup)


def _compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _truncate_text(value: str, limit: int) -> str:
    text = _compact_text(value)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _looks_noisy_text(value: str) -> bool:
    text = _compact_text(value)
    if not text:
        return False

    score = 0
    if len(re.findall(r"https?://\S+", text)) > 1:
        score += 2

    noisy_patterns = (
        r"\./[A-Za-z0-9._/-]+",
        r"\b(?:wget|sudo|copy|echo|hexo|apt|npm|pip|cmake|clang)\b",
        r"#\s*\d+",
        r"%[A-Za-z]",
        r"&&",
        r"[A-Za-z]:\\",
        r"</?\w",
        r"`",
    )
    for pattern in noisy_patterns:
        if re.search(pattern, text):
            score += 1
    return score >= 3


def _extract_excerpt(content_html: str) -> tuple[str, int, int, Optional[str]]:
    soup = BeautifulSoup(content_html, "html.parser")

    first_image = soup.find("img")
    cover_image = str(first_image.get("src")) if first_image and first_image.get("src") else None

    counting_soup = BeautifulSoup(content_html, "html.parser")
    for tag in counting_soup.select("script, style"):
        tag.decompose()

    raw_text = " ".join(segment.strip() for segment in counting_soup.stripped_strings if segment.strip())
    compact = _compact_text(raw_text)
    word_count = len(re.sub(r"\s+", "", compact))
    reading_minutes = max(1, math.ceil(max(word_count, 1) / 450))

    preview_soup = BeautifulSoup(content_html, "html.parser")
    for tag in preview_soup.select("script, style, pre, code, table"):
        tag.decompose()

    candidates: list[str] = []
    for node in preview_soup.select("p, li, blockquote"):
        text = _compact_text(node.get_text(" ", strip=True))
        if len(text) < 24 or _looks_noisy_text(text):
            continue
        candidates.append(text)
        if len(candidates) >= 3:
            break

    if not candidates:
        headings: list[str] = []
        for node in preview_soup.select("h1, h2, h3"):
            text = _compact_text(node.get_text(" ", strip=True))
            if not text or _looks_noisy_text(text):
                continue
            headings.append(text)
            if len(headings) >= 3:
                break
        joined = _compact_text(" ".join(headings))
        if joined:
            candidates.append(joined)

    if not candidates and compact:
        candidates.append(compact)

    excerpt = _truncate_text(candidates[0], 220) if candidates else ""
    return excerpt, word_count, reading_minutes, cover_image


def _sort_facets(counter: Counter[str]) -> tuple[BlogFacetItem, ...]:
    items = [BlogFacetItem(name=name, count=count) for name, count in counter.items()]
    items.sort(key=lambda item: (-item.count, item.name))
    return tuple(items)


def _load_post(path: Path) -> BlogPostRecord:
    metadata, body = _load_front_matter(path)
    relative_dir = path.parent.relative_to(_posts_root())
    storage_path = relative_dir.as_posix()

    published_at = _normalize_datetime(metadata.get("date"))
    if not published_at:
        raise ValueError("missing post date")
    updated_at = _normalize_datetime(metadata.get("updated"))

    published_dt = datetime.fromisoformat(published_at)
    title = str(metadata.get("title") or relative_dir.name).strip()
    url_segment = relative_dir.name
    post_path = "{:04d}/{:02d}/{:02d}/{}".format(
        published_dt.year,
        published_dt.month,
        published_dt.day,
        url_segment,
    )
    summary = _compact_text(str(metadata.get("summary") or "").strip())
    password = str(metadata.get("password") or "").strip()
    categories = _normalize_str_list(metadata.get("categories"))
    tags = _normalize_str_list(metadata.get("tags"))
    top = _normalize_int(metadata.get("top"))

    rendered_html = MARKDOWN_RENDERER(body)
    rewritten_html = _rewrite_rendered_html(rendered_html, storage_path)
    excerpt, word_count, reading_minutes, cover_image = _extract_excerpt(rewritten_html)

    if not summary or summary == ENCRYPTED_SUMMARY or _looks_noisy_text(summary):
        summary = excerpt
    summary = _truncate_text(summary, 220)

    return BlogPostRecord(
        title=title,
        storage_path=storage_path,
        post_path=post_path,
        url_path=f"/blog/{post_path}",
        published_at=published_at,
        updated_at=updated_at,
        summary=summary,
        excerpt=excerpt,
        categories=categories,
        tags=tags,
        cover_image=cover_image,
        word_count=word_count,
        reading_minutes=reading_minutes,
        top=top,
        content_html=rewritten_html,
        password=password,
        sort_key=datetime.fromisoformat(published_at),
    )


def _build_catalog() -> BlogCatalog:
    posts: list[BlogPostRecord] = []
    tags_counter: Counter[str] = Counter()
    categories_counter: Counter[str] = Counter()

    for path in sorted(_posts_root().rglob(POST_INDEX_NAME)):
        if not path.is_file():
            continue
        metadata, _ = _load_front_matter(path)
        if bool(metadata.get("draft")) or bool(metadata.get("hidden")):
            continue
        post = _load_post(path)
        posts.append(post)
        tags_counter.update(post.tags)
        categories_counter.update(post.categories)

    posts.sort(key=lambda item: (item.top, item.sort_key), reverse=True)
    post_map = {post.post_path: post for post in posts}

    return BlogCatalog(
        posts=tuple(posts),
        tags=_sort_facets(tags_counter),
        categories=_sort_facets(categories_counter),
        post_map=post_map,
    )


def _get_catalog() -> BlogCatalog:
    global BLOG_CACHE_DATA
    global BLOG_CACHE_SIGNATURE

    signature = _build_content_signature()
    with BLOG_LOCK:
        if BLOG_CACHE_DATA is not None and BLOG_CACHE_SIGNATURE == signature:
            return BLOG_CACHE_DATA

        BLOG_CACHE_DATA = _build_catalog()
        BLOG_CACHE_SIGNATURE = signature
        return BLOG_CACHE_DATA


def get_blog_index_payload() -> dict[str, Any]:
    catalog = _get_catalog()
    return {
        "posts": [post.to_summary() for post in catalog.posts],
        "tags": [{"name": item.name, "count": item.count} for item in catalog.tags],
        "categories": [{"name": item.name, "count": item.count} for item in catalog.categories],
        "total_posts": len(catalog.posts),
    }


def warmup_blog_catalog() -> int:
    catalog = _get_catalog()
    return len(catalog.posts)


def get_blog_post_detail_payload(year: int, month: int, day: int, post_id: str, password: str = "") -> dict[str, Any]:
    catalog = _get_catalog()
    post_path = "{:04d}/{:02d}/{:02d}/{}".format(year, month, day, post_id.strip())
    post = catalog.post_map.get(post_path)
    if post is None:
        raise FileNotFoundError(post_path)
    return post.to_detail(password=password)


def resolve_blog_asset_path(asset_path: str) -> Path:
    root = _posts_root()
    safe_relative = PurePosixPath(asset_path.strip("/"))
    candidate = (root / safe_relative).resolve()

    if root != candidate and root not in candidate.parents:
        raise FileNotFoundError(asset_path)
    if "assets" not in safe_relative.parts:
        raise FileNotFoundError(asset_path)
    if not candidate.exists() or not candidate.is_file():
        raise FileNotFoundError(asset_path)

    return candidate
