from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from common.schemas import CommonResponse
from modules.blog import (
    get_blog_index_payload,
    get_blog_post_detail_payload,
    resolve_blog_asset_path,
)

from .blog_schema import (
    BlogIndexData,
    BlogPostDetail,
    GetBlogIndexResponse,
    GetBlogPostDetailResponse,
)


router = APIRouter()


@router.get("/index", response_model=GetBlogIndexResponse, summary="查看博客索引")
async def get_blog_index():
    payload = get_blog_index_payload()
    return CommonResponse(data=BlogIndexData(**payload))


@router.get(
    "/posts/{year}/{month}/{day}/{post_id}",
    response_model=GetBlogPostDetailResponse,
    summary="查看博客详情",
)
async def get_blog_post_detail(year: int, month: int, day: int, post_id: str, password: str = ""):
    try:
        payload = get_blog_post_detail_payload(year=year, month=month, day=day, post_id=post_id, password=password)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="blog post not found") from exc
    return CommonResponse(data=BlogPostDetail(**payload))


@router.get("/assets/{asset_path:path}", summary="查看博客静态资源")
async def get_blog_asset(asset_path: str):
    try:
        path = resolve_blog_asset_path(asset_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="blog asset not found") from exc
    return FileResponse(path)
