---
name: promptbuddy
description: |
  PromptBuddy - 智能 Prompt 伙伴。每次用户提问时，必须先运行分析脚本，展示识别结果后再回答。
  
  ⚠️ 强制执行流程：
  1. 用户提问后，立即执行：cd ~/.openclaw/workspace/skills/promptbuddy && python3 scripts/smart_engine.py -f json "用户问题"
  2. 从返回的 JSON 中提取：intent（意图）、template（模板）、confidence（置信度）
  3. 在回答前展示：
     ┌─────────────────────────────────────┐
     │ 🤖 PromptBuddy 已优化               │
     │ 识别: [intent]                      │
     │ 模板: [template]                    │
     │ 置信度: [confidence]                │
     └─────────────────────────────────────┘
  4. 然后根据模板类型回答问题
  
  触发词：用户提问、需求描述、任务请求、问题咨询
---

# PromptBuddy - 智能 Prompt 伙伴

## ⚠️ 强制执行要求

**每次用户提问时，必须按以下流程执行：**

### 步骤 1：分析用户输入

```bash
cd ~/.openclaw/workspace/skills/promptbuddy && python3 scripts/smart_engine.py -f json "用户的问题"
```

### 步骤 2：提取分析结果

从 JSON 返回中提取：
- `intent`: 意图类型（reasoning/decomposition/criticism/simple）
- `template`: 模板名称（cot/decompose/criticize/base）
- `confidence`: 置信度（0.0-1.0）

### 步骤 3：展示 PromptBuddy 工作信息

```
┌─────────────────────────────────────┐
│ 🤖 PromptBuddy 已优化               │
│ 识别: [意图类型]                    │
│ 模板: [模板名称]                    │
│ 置信度: [数值]                      │
└─────────────────────────────────────┘
```

### 步骤 4：根据模板回答

- **cot（思维链）**：逐步推理分析
- **decompose（分解）**：拆解成步骤
- **criticize（检查）**：审核改进建议
- **base（基础）**：简洁专业回答

## 意图类型对照表

| intent | 类型名称 | 说明 |
|--------|---------|------|
| reasoning | 推理型 | 科学、原理、分析类问题 |
| decomposition | 分解型 | 项目、计划、流程类问题 |
| criticism | 检查型 | 审核、检查、改进类问题 |
| simple | 简单型 | 直接回答，无需优化 |

## 示例执行

**用户问**: "火箭如何上天？"

**执行**:
```bash
cd ~/.openclaw/workspace/skills/promptbuddy && python3 scripts/smart_engine.py -f json "火箭如何上天？"
```

**返回**:
```json
{
  "intent": "reasoning",
  "template": "cot",
  "confidence": 0.43
}
```

**输出**:
```
┌─────────────────────────────────────┐
│ 🤖 PromptBuddy 已优化               │
│ 识别: 推理型问题                    │
│ 模板: CoT（思维链）                 │
│ 置信度: 0.43                        │
└─────────────────────────────────────┘

作为推理专家，让我一步一步分析火箭发射升空的原理...
[继续回答]
```

## 特殊情况

### 简单查询（跳过优化）

如果 `action: "skip"`，直接回答，不展示 PromptBuddy 信息：

```json
{
  "action": "skip",
  "reason": "简单查询"
}
```

直接回答即可。

## 重要提醒

1. **必须先执行脚本**，不能跳过
2. **必须展示工作信息**，让用户感知
3. **根据模板类型调整回答方式**

---

**PromptBuddy - 要AI真懂你**