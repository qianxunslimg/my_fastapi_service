# Blog Content

博客内容统一放在 `posts/YYYY/文章目录/` 目录下。

物理目录名就是博客详情页 URL 的最后一段：
- 目录名优先使用文章标题生成，允许中文。
- 目录名里的非法路径字符会自动替换，避免文件系统问题。

每篇文章目录结构固定如下：

```text
posts/
  2026/
    我的新文章/
      index.md
      assets/
        example.png
```

`index.md` 使用 YAML front matter，正文推荐直接写 Markdown。

front matter 走最小字段原则：
- `date` 是常规必备字段。
- `title` 只有在文件夹名不能准确表示标题时才保留。
- `categories`、`tags`、`hidden`、`password` 只有实际需要时才保留。
- `top` 只有需要置顶排序时才保留，数字越大越靠前，同权重再按发布时间倒序。
- `slug`、`updated`、`summary`、`legacy_path` 默认不写。

图片和其它附件统一放在当前文章目录的 `assets/` 中，正文里用相对路径引用：

```md
![示例图片](./assets/example.png)
```

服务端会自动把这类相对路径解析成站内静态资源地址，所以旧文章和新文章都遵循同一套规则。

新建文章脚手架：

```bash
cd backend/app
python tools/create_blog_post.py --title "我的新文章" --category 开发随笔 --tag 记录
```

需要置顶时可以加排序权重：

```bash
cd backend/app
python tools/create_blog_post.py --title "我的新文章" --top 100
```
