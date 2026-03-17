# PromptBuddy - Your Intelligent Prompt Partner

> **Make AI Truly Understand You**
> OnlyPromptBuddy

[![GitHub stars](https://img.shields.io/github/stars/Steventsang18/promptbuddy?style=social)](https://github.com/Steventsang18/promptbuddy/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Steventsang18/promptbuddy?style=social)](https://github.com/Steventsang18/promptbuddy/network/members)
[![GitHub issues](https://img.shields.io/github/issues/Steventsang18/promptbuddy)](https://github.com/Steventsang18/promptbuddy/issues)
[![GitHub license](https://img.shields.io/github/license/Steventsang18/promptbuddy)](https://github.com/Steventsang18/promptbuddy/blob/main/LICENSE)

---

## Overview

PromptBuddy is an intelligent prompt engineering automation skill that:

- 🎯 **Auto-detect needs**: No trigger words required
- 🧠 **Semantic understanding**: Local TF-IDF engine
- 📊 **Smart decisions**: Hybrid detection strategy
- 📈 **Progressive learning**: Gets better the more you use it
- 🔄 **Hybrid feedback**: Explicit + implicit feedback

---

## Quick Start

### Install

```bash
# Via ClawHub
clawhub install promptbuddy

# Or clone from GitHub
git clone https://github.com/Steventsang18/promptbuddy.git
```

### Usage

```bash
# Auto mode (recommended)
./scripts/promptbuddy.sh "Help me write a product description"

# Force specific template
./scripts/promptbuddy.sh -t cot "How do rockets work?"

# JSON output
./scripts/promptbuddy.sh -f json "How to build a marketing system?"
```

---

## Features

### Smart Need Detection

| Input Type | Example | Processing |
|------------|---------|------------|
| Task-based | "Help me write a product intro" | ✅ Auto-optimize |
| Question-based | "How do rockets work?" | ✅ Auto-optimize |
| Simple query | "What's the weather?" | ⏭️ Skip |
| Greeting | "Hello!" | ⏭️ Skip |

### 4 Intelligent Templates

| Template | Use Case | Features |
|----------|----------|----------|
| **CoT** | Reasoning/Analysis | Step-by-step thinking |
| **Decompose** | Planning/Process | Task breakdown |
| **Criticize** | Review/Audit | Quality check |
| **Base** | General Q&A | Concise & professional |

### Progressive Learning

```
New User (<5 uses)    → Conservative strategy
Learning (5-20 uses)  → Adapts to preferences
Mature (20+ uses)     → Nearly fully automatic
```

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────┐
│  Need Detection     │  Filter if needed
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Intent Detection   │  Semantic + Keyword
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Decision Engine    │  Adaptive threshold
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Template Engine    │  Generate prompt
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Feedback System    │  Learn & improve
└─────────────────────┘
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Steventsang18/promptbuddy&type=Date)](https://star-history.com/#Steventsang18/promptbuddy&Date)

---

## Community

- 💬 **GitHub Discussions**: Feature requests, bug reports, usage sharing
- 🐛 **Issues**: Report problems or request features
- ⭐ **Star**: If you find it useful, please give it a star!

---

## Based On

"The Prompt Report: A Systematic Survey of Prompt Engineering Techniques"
- 58 text prompt techniques
- 40 multimodal techniques

---

## License

[MIT License](LICENSE)

---

**PromptBuddy - Make AI Truly Understand You**
OnlyPromptBuddy