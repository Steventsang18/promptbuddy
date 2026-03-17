# PromptBuddy - 智能 Prompt 伙伴

> **要AI真懂你**
> OnlyPromptBuddy

## 项目简介

PromptBuddy 是一个智能化的 Prompt 工程自动化技能，能够：

- 🎯 **自动识别需求**：无需触发词，系统自动判断用户输入是否需要优化
- 🧠 **语义理解**：基于 TF-IDF 的本地语义引擎，智能识别用户意图
- 📊 **智能决策**：混合检测策略，自动选择最佳模板
- 📈 **渐进学习**：越用越懂你，根据用户偏好持续优化
- 🔄 **混合反馈**：显式+隐式反馈机制，持续改进

---

## 快速开始

```bash
# 自动模式
./scripts/promptbuddy.sh "帮我写个产品介绍"

# 强制指定模板
./scripts/promptbuddy.sh -t cot "火箭如何上天？"

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

### 2. 四大智能模板

| 模板 | 适用场景 | 特点 |
|-----|---------|------|
| **CoT** | 科学/推理 | 逐步思考 |
| **Decompose** | 项目/流程 | 任务分解 |
| **Criticize** | 检查/审核 | 质量审查 |
| **Base** | 通用问答 | 简洁专业 |

### 3. 渐进式智能反馈

```
新用户（<5次）    → 保守策略
学习期（5-20次）  → 学习偏好
成熟期（>20次）   → 完全自动
```

---

## 文件结构

```
promptbuddy/
├── SKILL.md              # 技能描述
├── README.md             # 本文档
├── PROJECT_MEMORY.md     # 项目记忆
├── scripts/
│   ├── smart_engine.py   # 主引擎
│   ├── need_detector.py  # 需求识别
│   ├── semantic_engine.py# 语义引擎
│   ├── feedback.py       # 反馈系统
│   └── user_profile.py   # 用户偏好
└── templates/            # 模板文件
```

---

## 更新日志

### v2.2 (2026-03-17)
- ✅ 语义增强（TF-IDF）
- ✅ 混合检测策略
- ✅ 项目更名为 PromptBuddy

---

**PromptBuddy - 要AI真懂你**
OnlyPromptBuddy