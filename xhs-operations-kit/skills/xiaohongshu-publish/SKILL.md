---
name: xiaohongshu-publish
description: 小红书笔记发布工具 - 支持图文笔记和视频笔记发布、话题搜索、笔记搜索。Cookie登录、图片/视频上传、定时发布。当用户需要在小红书发布图文笔记、视频笔记、搜索小红书内容时使用此技能。
---

# 小红书笔记发布 (Xiaohongshu Publish)

## Overview

Python 实现的小红书笔记发布工具，支持图文笔记和视频笔记发布。基于 Web API，支持话题标签、定时发布、笔记搜索等功能。

## 快速开始

### 发布图文笔记
```bash
python3 xhs_publisher.py publish \
  --title "今日穿搭分享" \
  --desc "今天的穿搭灵感来自..." \
  --images photo1.jpg,photo2.jpg,photo3.jpg \
  --topics "穿搭,日常,ootd"
```

### 发布视频笔记
```bash
python3 xhs_publisher.py video \
  --title "旅行Vlog" \
  --desc "记录美好的一天" \
  --video vlog.mp4 \
  --cover cover.jpg
```

### 首次使用 - 配置Cookie
```bash
python3 xhs_publisher.py login
```

## 工作流决策树

```
用户需求
├── "发图文笔记" → python3 xhs_publisher.py publish --title xxx --images xxx
├── "发视频笔记" → python3 xhs_publisher.py video --title xxx --video xxx
├── "配置小红书账号" → python3 xhs_publisher.py login
├── "检查登录状态" → python3 xhs_publisher.py check
├── "搜索笔记" → python3 xhs_publisher.py search "关键词"
└── "Python调用" → from xhs_publisher import XhsClient
```

## 核心功能

### 1. Cookie 登录
获取方法: 浏览器登录 xiaohongshu.com → F12 → Network → 复制 Cookie 值
重要字段: `a1`, `web_session`, `webId`

### 2. 图文笔记发布
- 支持 1-18 张图片
- 标题限制 20 字
- 支持话题标签
- 支持定时发布
- 支持私密笔记

### 3. 视频笔记发布
- 支持 mp4 等格式
- 自定义封面图
- 话题标签

### 4. Python API
```python
from xhs_publisher import XhsClient

client = XhsClient(cookie="your_cookie_string")

# 发布图文
result = client.create_image_note(
    title="标题",
    desc="描述",
    image_paths=["img1.jpg", "img2.jpg"],
    topics=["话题1", "话题2"],
)

# 搜索笔记
notes = client.search_notes("关键词")
```

## ⚠️ 重要提示

小红书的 API 签名机制（x-s/x-t headers）较为复杂：
- 简单接口（如用户信息查询）可能使用简化签名即可
- 发布等核心接口可能需要完整签名（需要 Playwright 运行 JS）
- 如果遇到签名错误，可考虑安装 `xhs` 库: `pip install xhs`
- 完整签名参考: https://github.com/ReaJason/xhs

## 依赖

```bash
pip3 install requests
# 完整签名支持(可选):
# pip install xhs playwright && playwright install chromium
```

## Resources

### scripts/
- `xhs_publisher.py` - 小红书笔记发布核心工具 (CLI + Python API)

### references/
- 小红书 API 参考 (基于 ReaJason/xhs 项目)
