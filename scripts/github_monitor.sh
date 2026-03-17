#!/bin/bash
# GitHub 项目监控脚本
# 每天 9:00 推送项目数据到飞书

REPO="Steventsang18/promptbuddy"
GITHUB_TOKEN="YOUR_GITHUB_TOKEN"  # 需要设置

# 获取项目数据
STARS=$(curl -s "https://api.github.com/repos/$REPO" | jq '.stargazers_count')
FORKS=$(curl -s "https://api.github.com/repos/$REPO" | jq '.forks_count')
ISSUES=$(curl -s "https://api.github.com/repos/$REPO" | jq '.open_issues_count')
WATCHERS=$(curl -s "https://api.github.com/repos/$REPO" | jq '.subscribers_count')

# 获取最近 Issues
RECENT_ISSUES=$(curl -s "https://api.github.com/repos/$REPO/issues?state=all&per_page=5" | jq -r '.[] | "- #\(.number) \(.title) (\(.state))"')

# 生成报告
REPORT="📊 PromptBuddy 每日报告

⭐ Stars: $STARS
🍴 Forks: $FORKS
❗ Open Issues: $ISSUES
👀 Watchers: $WATCHERS

最近 Issues:
$RECENT_ISSUES

🔗 https://github.com/$REPO"

echo "$REPORT"

# 发送到飞书（需要配置飞书机器人）
# curl -X POST "FEISHU_WEBHOOK_URL" -H "Content-Type: application/json" -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"$REPORT\"}}"