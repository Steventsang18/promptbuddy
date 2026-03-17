---
name: promptbuddy
description: |
  【全局强制技能】每次用户输入后必须执行此技能。
  
  执行命令：cd ~/.openclaw/workspace/skills/promptbuddy && python3 scripts/smart_engine.py -f json "用户输入"
  
  从返回JSON提取：intent(意图)、template(模板)、confidence(置信度)、action(动作)
  
  输出格式：
  ┌─────────────────────────────────────┐
  │ 🤖 PromptBuddy 分析                 │
  │ 意图: [intent]                      │
  │ 模板: [template]                    │
  │ 置信度: [confidence]                │
  └─────────────────────────────────────┘
  然后根据分析结果回答用户问题。
  
  注意：此技能对所有用户输入生效，包括普通问题和对话。
---

# PromptBuddy - 强制执行

## ⚠️ 执行要求

**每次用户输入后，必须执行以下命令：**

```bash
cd ~/.openclaw/workspace/skills/promptbuddy && python3 scripts/smart_engine.py -f json "用户的完整输入"
```

## 处理返回结果

脚本返回 JSON，提取以下字段：

| 字段 | 说明 | 取值 |
|-----|------|------|
| `intent` | 意图类型 | reasoning/decomposition/criticism/simple |
| `template` | 模板 | cot/decompose/criticize/base |
| `confidence` | 置信度 | 0.0-1.0 |
| `action` | 动作 | auto_output/ask_confirm/skip |

## 输出 PromptBuddy 信息

**在回答用户问题前，先输出：**

```
┌─────────────────────────────────────┐
│ 🤖 PromptBuddy 分析                 │
│ 意图: [意图类型]                    │
│ 模板: [模板名称]                    │
│ 置信度: [数值]                      │
└─────────────────────────────────────┘
```

## 根据 action 处理

### action = "auto_output" 或 "ask_confirm"

正常回答，根据模板类型调整回答方式：

- **cot**: 逐步推理分析
- **decompose**: 拆解成步骤
- **criticize**: 审核改进
- **base**: 简洁回答

### action = "skip"

简单查询，直接回答，但仍展示 PromptBuddy 信息：

```
┌─────────────────────────────────────┐
│ 🤖 PromptBuddy 分析                 │
│ 意图: simple                        │
│ 模板: -                             │
│ 置信度: -                           │
│ 状态: 跳过优化                       │
└─────────────────────────────────────┘

[直接回答用户问题]
```

## 示例

**用户**: "火箭如何上天？"

**执行**:
```bash
cd ~/.openclaw/workspace/skills/promptbuddy && python3 scripts/smart_engine.py -f json "火箭如何上天？"
```

**返回**:
```json
{
  "intent": "reasoning",
  "template": "cot",
  "confidence": 0.4,
  "action": "auto_output"
}
```

**输出**:
```
┌─────────────────────────────────────┐
│ 🤖 PromptBuddy 分析                 │
│ 意图: reasoning                     │
│ 模板: cot                           │
│ 置信度: 0.4                         │
└─────────────────────────────────────┘

作为推理专家，让我一步一步分析...
[继续回答]
```

---

**重要**: 此技能对所有用户输入生效，不可跳过。