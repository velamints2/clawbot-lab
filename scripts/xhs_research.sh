#!/bin/bash
# 小红书调研脚本 - 心跳触发
# 每 10 分钟执行一次，浏览首页推荐流

echo "=== 调研开始：$(date '+%Y-%m-%d %H:%M:%S') ===" >> /Users/macbookair/.openclaw/workspaceLocal\ \(this\ machine\)/memory/xhs-research-cron.log

# 打开小红书首页推荐流
open "https://www.xiaohongshu.com/explore"

echo "调研完成：$(date '+%Y-%m-%d %H:%M:%S')" >> /Users/macbookair/.openclaw/workspaceLocal\ \(this\ machine\)/memory/xhs-research-cron.log
