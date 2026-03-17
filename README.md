# PromptBuddy - 智能 Prompt 伙伴

> **要AI真懂你**
> OnlyPromptBuddy

[![GitHub stars](https://img.shields.io/github/stars/Steventsang18/promptbuddy?style=social)](https://github.com/Steventsang18/promptbuddy/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Steventsang18/promptbuddy?style=social)](https://github.com/Steventsang18/promptbuddy/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Steventsang18/promptbuddy)](https://github.com/Steventsang18/promptbuddy/issues)
[![GitHub license](https://img.shields.io/github/license/Steventsang18/promptbuddy)](https://github.com/Steventsang18/promptbuddy/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/Steventsang18/promptbuddy?include_prereleases)](https://github.com/Steventsang18/promptbuddy/releases)

---

## 项目简介

PromptBuddy 是一个智能化的 Prompt 工程自动化技能，能够：

- 🎯 **自动识别需求**：无需触发词，系统自动判断用户输入是否需要优化
- 🧠 **语义理解**：基于 TF-IDF 的本地语义引擎，智能识别用户意图
- 📊 **智能决策**：混合检测策略，自动选择最佳模板
- 📈 **渐进学习**：越用越懂你，根据用户偏好持续优化
- 🔄 **混合反馈**：显式+隐式反馈机制，持续改进

---

## 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install promptbuddy

# 或从 GitHub 克隆
git clone https://github.com/Steventsang18/promptbuddy.git
```

### 使用

```bash
# 自动模式（推荐）
./scripts/promptbuddy.sh "帮我写个产品介绍"

# 强制指定模板
./scripts/promptbuddy.sh -t cot "火箭如何上天？"

# JSON 格式输出
./scripts/promptbuddy.sh -f json "如何建立运营体系？"

# 查看统计
./scripts/promptbuddy.sh --stats
```

---

## 核心功能

### 1. 智能需求识别

| 输入类型 | 示例 | 处理方式 |
|---------|------|---------|
| 任务型 | "帮我写个产品介绍" | ✅ 自动优化 |
| 问句型 | "火箭如何上天？" | ✅ 自动优化 |
| 简单查询 | "今天天气怎么样" | ⏭️ 跳过优化 |
| 问候语 | "你好，在吗？" | ⏭️ 跳过优化 |

### 2. 四大智能模板

| 模板 | 适用场景 | 特点 |
|-----|---------|------|
| **CoT** | 科学/推理/分析 | 逐步思考，深度推理 |
| **Decompose** | 项目/计划/流程 | 任务分解，步骤指南 |
| **Criticize** | 检查/审核/优化 | 质量审查，改进建议 |
| **Base** | 通用问答 | 简洁专业，清晰回答 |

### 3. 渐进式智能反馈

```
新用户（<5次）    → 保守策略，低置信度时确认
学习期（5-20次）  → 系统学习用户偏好
成熟期（>20次）   → 几乎全自动，完全个性化
```

---

## 技术架构

```
用户输入
    │
    ▼
┌─────────────────────┐
│   需求识别层         │  判断是否需要优化
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   意图识别层         │  语义 + 关键词混合检测
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   决策层             │  自适应阈值 + 用户偏好
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   模板生成层         │  生成优化后的 Prompt
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   反馈系统           │  收集反馈，持续优化
└─────────────────────┘
```

---

## 文件结构

```
promptbuddy/
├── SKILL.md              # 技能描述
├── README.md             # 本文档
├── README_EN.md          # 英文文档
├── LICENSE               # MIT 许可证
├── config.json           # 版本配置
├── scripts/
│   ├── smart_engine.py   # 主引擎
│   ├── need_detector.py  # 需求识别
│   ├── semantic_engine.py# 语义引擎
│   ├── feedback.py       # 反馈系统
│   └── user_profile.py   # 用户偏好
├── templates/            # 模板文件
└── tests/                # 测试脚本
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Steventsang18/promptbuddy&type=Date)](https://star-history.com/#Steventsang18/promptbuddy&Date)

---

## 社区

- 💬 **GitHub Discussions**: 讨论功能建议、Bug 报告、使用分享
- 🐛 **Issues**: 报告问题或请求新功能
- ⭐ **Star**: 如果觉得有用，请给个 Star！

---

## 基于《The Prompt Report》

本技能基于论文《The Prompt Report: A Systematic Survey of Prompt Engineering Techniques》：
- 58 种文本 Prompt 技术
- 40 种多模态 Prompt 技术

---

## 许可证

[MIT License](LICENSE)

---

## 联系方式

**项目作者**: 曾鹏祥
**GitHub**: https://github.com/Steventsang18/promptbuddy

---

**PromptBuddy - 要AI真懂你**
OnlyPromptBuddy