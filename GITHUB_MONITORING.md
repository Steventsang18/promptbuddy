# GitHub 项目监控方案

## 一、即时通知（推荐）

### GitHub Mobile App

**下载**：
- iOS: App Store 搜索 "GitHub"
- Android: Google Play 或应用商店

**设置**：
1. 登录 GitHub 账号
2. 进入 Notifications 设置
3. 开启 PromptBuddy 仓库通知
4. 设置推送：Stars, Issues, Pull Requests, Releases

**效果**：
- ⭐ 新 Star → 即时推送
- 🐛 新 Issue → 即时推送
- 📝 新 PR → 即时推送

---

## 二、每日报告（自动化）

### 监控脚本

**位置**: `scripts/github_monitor.sh`

**功能**：
- Stars/Forks/Issues 数量统计
- 最近 Issues 列表
- 发送到飞书群

### 设置每日报告

```bash
# 添加 cron 任务
# 每天 9:00 执行
openclaw cron add \
  --name "promptbuddy-github-report" \
  --cron "0 9 * * *" \
  --message "查看 GitHub 监控脚本输出"
```

---

## 三、飞书机器人推送

### 创建飞书机器人

1. **创建飞书群**：PromptBuddy 运营群

2. **添加自定义机器人**：
   - 群设置 → 群机器人 → 添加机器人 → 自定义机器人
   - 复制 Webhook 地址

3. **配置推送**：
   ```bash
   # 编辑监控脚本
   FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
   ```

---

## 四、快速查看面板

### GitHub 自带

- **Insights → Traffic**: 访问量、克隆量
- **Insights → Pulse**: 周活跃度
- **Actions**: 构建状态

### 第三方工具

| 工具 | 链接 | 功能 |
|-----|------|------|
| **Repography** | repography.com | 生成项目动态图 |
| **Star History** | star-history.com | Star 增长曲线 |
| **GitHub Readme Stats** | github-readme-stats | README 统计卡片 |

---

## 五、添加到 README

### 统计徽章

```markdown
![GitHub stars](https://img.shields.io/github/stars/Steventsang18/promptbuddy?style=social)
![GitHub forks](https://img.shields.io/github/forks/Steventsang18/promptbuddy?style=social)
![GitHub issues](https://img.shields.io/github/issues/Steventsang18/promptbuddy)
![GitHub license](https://img.shields.io/github/license/Steventsang18/promptbuddy)
```

### Star History 图表

```markdown
[![Star History Chart](https://api.star-history.com/svg?repos=Steventsang18/promptbuddy&type=Date)](https://star-history.com/#Steventsang18/promptbuddy&Date)
```

---

## 推荐组合

```
📱 手机端：GitHub Mobile App（即时通知）
📊 每日报告：飞书机器人（每日 9:00）
🔍 详细分析：GitHub Insights + Star History
📝 README：徽章 + 统计卡片
```

---

_更新时间: 2026-03-17_