from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from common.schemas import CommonResponse


class BlogFacetItem(BaseModel):
    name: str = Field(..., description="分类或标签名称")
    count: int = Field(..., description="文章数量")


class BlogPostSummary(BaseModel):
    title: str = Field(..., description="文章标题")
    post_path: str = Field(..., description="文章相对路径")
    url_path: str = Field(..., description="站内博客路径")
    published_at: str = Field(..., description="发布时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")
    summary: str = Field(..., description="文章摘要")
    excerpt: str = Field(..., description="文章摘录")
    categories: List[str] = Field(default_factory=list, description="分类列表")
    tags: List[str] = Field(default_factory=list, description="标签列表")
    cover_image: Optional[str] = Field(default=None, description="封面图地址")
    word_count: int = Field(..., description="内容字数")
    reading_minutes: int = Field(..., description="预估阅读分钟数")
    top: int = Field(default=0, description="置顶排序权重")
    password_required: bool = Field(default=False, description="是否需要密码")
    password_unlocked: bool = Field(default=True, description="当前响应是否已解锁")


class BlogPostDetail(BlogPostSummary):
    content_html: str = Field(..., description="渲染后的文章 HTML")


class BlogIndexData(BaseModel):
    posts: List[BlogPostSummary] = Field(default_factory=list, description="文章列表")
    tags: List[BlogFacetItem] = Field(default_factory=list, description="标签统计")
    categories: List[BlogFacetItem] = Field(default_factory=list, description="分类统计")
    total_posts: int = Field(..., description="文章总数")


GetBlogIndexResponse = CommonResponse[BlogIndexData]
GetBlogPostDetailResponse = CommonResponse[BlogPostDetail]
