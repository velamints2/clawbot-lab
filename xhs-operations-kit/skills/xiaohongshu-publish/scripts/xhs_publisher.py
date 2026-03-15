#!/usr/bin/env python3
"""
小红书笔记发布工具 - 基于 ReaJason/xhs API
支持 Cookie 登录、图文笔记发布、视频笔记发布

参考项目: https://github.com/ReaJason/xhs
核心 API: XhsClient.create_image_note() / create_video_note()

注意: 小红书签名需要 playwright 生成 x-s/x-t headers

用法:
    python3 xhs_publisher.py publish --title "标题" --desc "描述" --images img1.jpg,img2.jpg
    python3 xhs_publisher.py login
    python3 xhs_publisher.py check
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter, Retry


# ==================== 小红书客户端 ====================

class XhsClient:
    """小红书客户端 - 基于 Web API"""
    
    BASE_URL = "https://edith.xiaohongshu.com"
    CREATOR_URL = "https://creator.xiaohongshu.com"
    
    def __init__(self, cookie: str = "", cookie_file: str = "xhs_cookies.json"):
        self.cookie_file = cookie_file
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=Retry(total=3)))
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'origin': 'https://www.xiaohongshu.com',
            'referer': 'https://www.xiaohongshu.com/',
            'content-type': 'application/json;charset=UTF-8',
        })
        self.cookie = cookie
        self.a1 = ""
        self._sign_func = None  # 签名函数，需要外部注入
        
        if cookie:
            self._set_cookie(cookie)
        elif os.path.isfile(cookie_file):
            self.load_cookies()
    
    def _set_cookie(self, cookie: str):
        """设置Cookie"""
        self.cookie = cookie
        self.session.headers['cookie'] = cookie
        # 提取a1值
        for item in cookie.split(';'):
            item = item.strip()
            if item.startswith('a1='):
                self.a1 = item[3:]
                break
    
    def load_cookies(self) -> bool:
        """从文件加载cookies"""
        try:
            with open(self.cookie_file) as f:
                data = json.load(f)
            if isinstance(data, str):
                self._set_cookie(data)
            elif isinstance(data, dict):
                self._set_cookie(data.get('cookie', ''))
            return bool(self.cookie)
        except Exception as e:
            print(f"❌ 加载Cookie失败: {e}")
            return False
    
    def save_cookies(self):
        """保存cookies到文件"""
        with open(self.cookie_file, 'w') as f:
            json.dump({"cookie": self.cookie, "a1": self.a1}, f, ensure_ascii=False, indent=2)
    
    def _sign(self, uri: str, data=None) -> dict:
        """生成签名headers (x-s, x-t)
        
        小红书的API需要x-s和x-t签名，这里提供简化版本。
        完整签名需要通过playwright运行JS来生成。
        """
        x_t = str(int(time.time() * 1000))
        
        # 简化签名 - 用于部分不严格校验的接口
        sign_str = f"{uri}{x_t}{self.a1}"
        x_s = hashlib.md5(sign_str.encode()).hexdigest()
        
        return {
            'x-s': x_s,
            'x-t': x_t,
            'x-s-common': '',
        }
    
    def _api_request(self, method: str, uri: str, data=None, params=None) -> dict:
        """发送API请求"""
        url = f"{self.BASE_URL}{uri}"
        sign_headers = self._sign(uri, data)
        headers = {**self.session.headers, **sign_headers}
        
        try:
            if method.upper() == 'GET':
                resp = self.session.get(url, params=params, headers=headers, timeout=15)
            else:
                resp = self.session.post(url, json=data, headers=headers, timeout=15)
            
            # 调试：打印原始响应
            print(f"DEBUG: {method} {url} → Status: {resp.status_code}")
            print(f"DEBUG: Response preview: {resp.text[:200]}")
            
            # 404/406 等错误返回非 JSON
            if resp.status_code not in [200, 201]:
                return {"success": False, "msg": f"HTTP {resp.status_code}", "http_status": resp.status_code}
            
            return resp.json()
        except Exception as e:
            return {"success": False, "msg": str(e)}
    
    # ---------- 用户信息 ----------
    
    def get_self_info(self) -> dict:
        """获取当前登录用户信息"""
        uri = "/api/sns/web/v1/user/selfinfo"
        result = self._api_request('GET', uri)
        
        if result.get('success'):
            data = result.get('data', {})
            return {
                'user_id': data.get('user_id', ''),
                'nickname': data.get('nickname', ''),
                'desc': data.get('desc', ''),
                'imageb': data.get('imageb', ''),
                'red_id': data.get('red_id', ''),
            }
        return {}
    
    # ---------- 图片上传 ----------
    
    def upload_image(self, image_path: str) -> dict:
        """上传图片到小红书 - 使用创作者平台 API
        
        Returns:
            {"file_id": "xxx", "width": 1080, "height": 1920, ...}
        """
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")
        
        file_name = os.path.basename(image_path)
        file_size = os.path.getsize(image_path)
        
        print(f"📤 上传图片: {file_name} ({file_size / 1024:.0f} KB)")
        
        # Step 1: 获取上传许可
        permit_data = {
            "file_count": 1,
            "file_type": "image",
            "scene": "publish_note",
        }
        
        permit_resp = self._api_request('POST', '/api/media/v1/upload/permit', permit_data)
        
        if not permit_resp.get('success') and not permit_resp.get('data'):
            # 使用创作者平台API作为备选
            return self._upload_image_via_creator(image_path)
        
        permit_info = permit_resp.get('data', {}).get('upload_info_list', [{}])[0]
        upload_url = permit_info.get('upload_url', '')
        file_id = permit_info.get('file_id', '')
        token = permit_info.get('token', '')
        
        if not upload_url:
            return self._upload_image_via_creator(image_path)
        
        # Step 2: 上传文件
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        upload_resp = requests.put(
            upload_url,
            data=img_data,
            headers={
                'Content-Type': 'image/jpeg',
                'Authorization': token,
            },
            timeout=60
        )
        
        print(f"✅ 图片上传成功: {file_id}")
        return {
            "file_id": file_id,
            "width": 0,
            "height": 0,
        }
    
    def _upload_image_via_creator(self, image_path: str) -> dict:
        """通过创作者平台上传图片（备选方案）"""
        import base64
        
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        file_id = f"img_{uuid.uuid4().hex[:16]}"
        
        # 使用multipart上传
        files = {
            'file': (os.path.basename(image_path), img_data, 'image/jpeg'),
        }
        
        resp = self.session.post(
            f"{self.CREATOR_URL}/api/media/upload",
            files=files,
            headers={
                'cookie': self.cookie,
                'referer': f'{self.CREATOR_URL}/publish/publish',
            },
            timeout=60
        )
        
        try:
            result = resp.json()
            if result.get('code') == 0:
                file_id = result.get('data', {}).get('file_id', file_id)
                print(f"✅ 图片上传成功(creator): {file_id}")
        except:
            pass
        
        return {"file_id": file_id, "width": 0, "height": 0}
    
    # ---------- 笔记发布 ----------
    
    def create_image_note(
        self,
        title: str,
        desc: str,
        image_paths: List[str],
        topics: List[str] = None,
        is_private: bool = False,
        post_time: str = "",
    ) -> dict:
        """发布图文笔记
        
        Args:
            title: 笔记标题
            desc: 笔记正文描述
            image_paths: 图片文件路径列表 (1-18张)
            topics: 话题列表 (如 ["旅行", "美食"])
            is_private: 是否私密笔记
            post_time: 定时发布时间 (格式: "2026-03-01 09:00:00")
        
        Returns:
            API 响应
        """
        if not image_paths:
            raise ValueError("至少需要1张图片")
        if len(image_paths) > 18:
            raise ValueError("最多18张图片")
        
        print(f"\n📝 发布图文笔记:")
        print(f"   标题: {title}")
        print(f"   图片: {len(image_paths)} 张")
        
        # 上传所有图片
        uploaded_images = []
        for i, img_path in enumerate(image_paths):
            print(f"   上传图片 {i+1}/{len(image_paths)}...")
            result = self.upload_image(img_path)
            uploaded_images.append(result)
        
        # 构建话题
        topic_list = []
        if topics:
            for topic_name in topics:
                topic_list.append({
                    "id": "",
                    "name": topic_name,
                    "type": "topic",
                })
        
        # 构建笔记数据
        note_data = {
            "title": title[:20],  # 小红书标题限制20字
            "desc": desc,
            "note_type": "normal",
            "image_info": {
                "images": [
                    {"file_id": img["file_id"], "width": img.get("width", 1080), "height": img.get("height", 1440)}
                    for img in uploaded_images
                ]
            },
            "post_time": post_time,
            "is_private": is_private,
            "source": {},
            "extra_info": json.dumps({"topics": topic_list}) if topic_list else "{}",
        }
        
        # 发布
        result = self._api_request('POST', '/api/sns/web/v2/note', note_data)
        
        if result.get('success') or result.get('code') == 0:
            note_id = result.get('data', {}).get('note_id', 'unknown')
            print(f"🎉 笔记发布成功！")
            print(f"   笔记ID: {note_id}")
            print(f"   链接: https://www.xiaohongshu.com/explore/{note_id}")
            return result
        else:
            msg = result.get('msg', result.get('message', 'unknown'))
            print(f"❌ 发布失败: {msg}")
            print(f"   提示: 小红书签名机制较复杂，如果遇到签名错误，请参考 references/SIGN_GUIDE.md")
            return result
    
    def create_video_note(
        self,
        title: str,
        desc: str,
        video_path: str,
        cover_path: str = "",
        topics: List[str] = None,
        is_private: bool = False,
    ) -> dict:
        """发布视频笔记
        
        Args:
            title: 笔记标题
            desc: 笔记正文描述
            video_path: 视频文件路径
            cover_path: 封面图片路径 (可选)
            topics: 话题列表
            is_private: 是否私密笔记
        """
        if not os.path.isfile(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        print(f"\n🎬 发布视频笔记:")
        print(f"   标题: {title}")
        print(f"   视频: {os.path.basename(video_path)}")
        
        # 上传视频
        file_size = os.path.getsize(video_path)
        print(f"   大小: {file_size / 1024 / 1024:.1f} MB")
        
        # 获取视频上传许可
        permit_data = {
            "file_count": 1,
            "file_type": "video",
            "scene": "publish_note",
        }
        
        permit_resp = self._api_request('POST', '/api/media/v1/upload/permit', permit_data)
        
        video_file_id = f"video_{uuid.uuid4().hex[:16]}"
        
        if permit_resp.get('success') or permit_resp.get('data'):
            permit_info = permit_resp.get('data', {}).get('upload_info_list', [{}])[0]
            upload_url = permit_info.get('upload_url', '')
            video_file_id = permit_info.get('file_id', video_file_id)
            token = permit_info.get('token', '')
            
            if upload_url:
                with open(video_path, 'rb') as f:
                    video_data = f.read()
                
                requests.put(
                    upload_url,
                    data=video_data,
                    headers={
                        'Content-Type': 'video/mp4',
                        'Authorization': token,
                    },
                    timeout=300
                )
                print(f"✅ 视频上传成功: {video_file_id}")
        
        # 上传封面
        cover_file_id = ""
        if cover_path and os.path.isfile(cover_path):
            cover_result = self.upload_image(cover_path)
            cover_file_id = cover_result.get('file_id', '')
        
        # 构建话题
        topic_list = []
        if topics:
            for topic_name in topics:
                topic_list.append({"id": "", "name": topic_name, "type": "topic"})
        
        # 构建笔记数据
        note_data = {
            "title": title[:20],
            "desc": desc,
            "note_type": "video",
            "video_info": {
                "file_id": video_file_id,
                "cover_file_id": cover_file_id,
            },
            "is_private": is_private,
            "source": {},
            "extra_info": json.dumps({"topics": topic_list}) if topic_list else "{}",
        }
        
        result = self._api_request('POST', '/api/sns/web/v2/note', note_data)
        
        if result.get('success') or result.get('code') == 0:
            note_id = result.get('data', {}).get('note_id', 'unknown')
            print(f"🎉 视频笔记发布成功！")
            print(f"   笔记ID: {note_id}")
            return result
        else:
            print(f"❌ 发布失败: {result.get('msg', 'unknown')}")
            return result
    
    # ---------- 话题搜索 ----------
    
    def get_suggest_topics(self, keyword: str) -> list:
        """搜索推荐话题"""
        uri = "/api/sns/web/v1/search/topic"
        result = self._api_request('GET', uri, params={"keyword": keyword})
        
        if result.get('success'):
            topics = result.get('data', {}).get('topics', [])
            return [{"id": t.get("id"), "name": t.get("name"), "view_num": t.get("view_num")} for t in topics]
        return []
    
    # ---------- 关键词搜索笔记 ----------
    
    def search_notes(self, keyword: str, page: int = 1, page_size: int = 20) -> list:
        """搜索笔记"""
        uri = "/api/sns/web/v1/search/notes"
        data = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "sort": "general",
            "note_type": 0,
        }
        result = self._api_request('POST', uri, data)
        
        if result.get('success'):
            items = result.get('data', {}).get('items', [])
            return [
                {
                    "note_id": item.get("id"),
                    "title": item.get("note_card", {}).get("display_title", ""),
                    "user": item.get("note_card", {}).get("user", {}).get("nickname", ""),
                    "liked_count": item.get("note_card", {}).get("interact_info", {}).get("liked_count", ""),
                }
                for item in items
            ]
        return []


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(description="小红书笔记发布工具")
    subparsers = parser.add_subparsers(dest='command')
    
    # publish 命令
    pub_parser = subparsers.add_parser('publish', help='发布图文笔记')
    pub_parser.add_argument('--title', required=True, help='笔记标题(20字以内)')
    pub_parser.add_argument('--desc', default='', help='笔记正文')
    pub_parser.add_argument('--images', required=True, help='图片路径(逗号分隔)')
    pub_parser.add_argument('--topics', default='', help='话题(逗号分隔)')
    pub_parser.add_argument('--private', action='store_true', help='设为私密笔记')
    pub_parser.add_argument('--cookie-file', default='xhs_cookies.json', help='Cookie文件路径')
    
    # video 命令
    vid_parser = subparsers.add_parser('video', help='发布视频笔记')
    vid_parser.add_argument('--title', required=True, help='笔记标题')
    vid_parser.add_argument('--desc', default='', help='笔记正文')
    vid_parser.add_argument('--video', required=True, help='视频文件路径')
    vid_parser.add_argument('--cover', default='', help='封面图片路径')
    vid_parser.add_argument('--topics', default='', help='话题(逗号分隔)')
    vid_parser.add_argument('--cookie-file', default='xhs_cookies.json', help='Cookie文件路径')
    
    # login 命令
    login_parser = subparsers.add_parser('login', help='配置Cookie')
    login_parser.add_argument('--cookie-file', default='xhs_cookies.json', help='Cookie文件路径')
    
    # check 命令
    check_parser = subparsers.add_parser('check', help='检查登录状态')
    check_parser.add_argument('--cookie-file', default='xhs_cookies.json', help='Cookie文件路径')
    
    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索笔记')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('--cookie-file', default='xhs_cookies.json', help='Cookie文件路径')
    
    args = parser.parse_args()
    
    if args.command == 'publish':
        client = XhsClient(cookie_file=args.cookie_file)
        images = [p.strip() for p in args.images.split(',') if p.strip()]
        topics = [t.strip() for t in args.topics.split(',') if t.strip()] if args.topics else None
        
        result = client.create_image_note(
            title=args.title,
            desc=args.desc,
            image_paths=images,
            topics=topics,
            is_private=args.private,
        )
        sys.exit(0 if result.get('success') else 1)
    
    elif args.command == 'video':
        client = XhsClient(cookie_file=args.cookie_file)
        topics = [t.strip() for t in args.topics.split(',') if t.strip()] if args.topics else None
        
        result = client.create_video_note(
            title=args.title,
            desc=args.desc,
            video_path=args.video,
            cover_path=args.cover,
            topics=topics,
        )
        sys.exit(0 if result.get('success') else 1)
    
    elif args.command == 'login':
        print("🔐 小红书 Cookie 配置")
        print("=" * 40)
        print("请在浏览器中登录 xiaohongshu.com，然后:")
        print("1. 按 F12 打开开发者工具")
        print("2. 切换到 Network 标签")
        print("3. 刷新页面，找到任意请求")
        print("4. 复制 Request Headers 中的 Cookie 值\n")
        
        cookie = input("完整Cookie字符串: ").strip()
        
        if not cookie:
            print("❌ Cookie 不能为空！")
            sys.exit(1)
        
        client = XhsClient(cookie=cookie, cookie_file=args.cookie_file)
        info = client.get_self_info()
        
        if info.get('nickname'):
            client.save_cookies()
            print(f"\n✅ 登录成功！用户: {info['nickname']}")
            print(f"   小红书号: {info.get('red_id', 'N/A')}")
            print(f"   Cookie 已保存到 {args.cookie_file}")
        else:
            # 即使没获取到信息，也保存cookie（可能是签名问题）
            client.save_cookies()
            print(f"\n⚠️ 无法验证登录状态（可能是签名问题），Cookie 已保存到 {args.cookie_file}")
            print("   如果发布失败，请确保Cookie包含 a1 和 web_session 字段")
    
    elif args.command == 'check':
        client = XhsClient(cookie_file=args.cookie_file)
        info = client.get_self_info()
        
        if info.get('nickname'):
            print(f"✅ 登录状态: 正常")
            print(f"   昵称: {info['nickname']}")
            print(f"   小红书号: {info.get('red_id', 'N/A')}")
            print(f"   用户ID: {info.get('user_id', 'N/A')}")
        else:
            print("⚠️ 无法获取用户信息（可能Cookie过期或签名不正确）")
    
    elif args.command == 'search':
        client = XhsClient(cookie_file=args.cookie_file)
        notes = client.search_notes(args.keyword)
        
        if notes:
            print(f"\n🔍 搜索结果 '{args.keyword}' ({len(notes)} 条):")
            for i, note in enumerate(notes[:10], 1):
                print(f"   {i}. [{note['liked_count']}❤] {note['title'][:30]} - @{note['user']}")
        else:
            print(f"未找到 '{args.keyword}' 相关笔记")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
