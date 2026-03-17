# PromptBuddy - Your Intelligent Prompt Partner

> **Make AI Truly Understand You**
> OnlyPromptBuddy

## Overview

PromptBuddy is an intelligent prompt engineering automation skill that:

- 🎯 **Auto-detect needs**: No trigger words required, automatically identifies if optimization is needed
- 🧠 **Semantic understanding**: Local TF-IDF engine for intelligent intent recognition
- 📊 **Smart decisions**: Hybrid detection strategy for optimal template selection
- 📈 **Progressive learning**: Gets better the more you use it
- 🔄 **Hybrid feedback**: Explicit + implicit feedback for continuous improvement

---

## Quick Start

### Automatic Mode (Recommended)

```bash
# Just speak naturally
./scripts/promptbuddy.sh "Help me write a product description"

# The system will:
# 1. Detect if optimization is needed
# 2. Identify your intent
# 3. Select the best template
# 4. Generate optimized prompt
```

### Manual Mode

```bash
# Force a specific template
./scripts/promptbuddy.sh -t cot "How do rockets reach space?"

# JSON output
./scripts/promptbuddy.sh -f json "How to build a marketing system?"

# View statistics
./scripts/promptbuddy.sh --stats
./scripts/promptbuddy.sh --feedback-stats
```

---

## Four Intelligent Templates

| Template | Use Case | Features |
|----------|----------|----------|
| **CoT** | Science/Reasoning/Analysis | Step-by-step thinking |
| **Decompose** | Project/Plan/Process | Task breakdown |
| **Criticize** | Review/Audit/Optimize | Quality check |
| **Base** | General Q&A | Concise and professional |

---

## Features

### 1. Smart Need Detection

| Input Type | Example | Processing |
|------------|---------|------------|
| Task-based | "Help me write a product intro" | ✅ Auto-optimize |
| Question-based | "How do rockets work?" | ✅ Auto-optimize |
| Simple query | "What's the weather today?" | ⏭️ Skip |
| Greeting | "Hello, are you there?" | ⏭️ Skip |

### 2. Progressive Intelligent Feedback

```
New User (<5 uses)    → Conservative strategy
Learning (5-20 uses)  → System learns your preferences
Mature (20+ uses)     → Nearly fully automatic
```

### 3. Semantic Enhancement

- **Local TF-IDF Engine**: No model download required
- **Hybrid Detection**: Combines semantic and keyword matching
- **Smart Fusion**: Automatically selects the best method

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────┐
│  Need Detection     │  Filter if optimization needed
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Intent Detection   │  Semantic + Keyword hybrid
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Decision Engine    │  Adaptive threshold + User preference
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Template Engine    │  Generate optimized prompt
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Feedback System    │  Collect and learn
└─────────────────────┘
```

---

## File Structure

```
promptbuddy/
├── SKILL.md              # Skill description
├── README.md             # This document
├── README_CN.md          # Chinese documentation
├── config.json           # Version management
├── scripts/
│   ├── smart_engine.py   # Main engine
│   ├── need_detector.py  # Need detection
│   ├── semantic_engine.py# Semantic engine
│   ├── feedback.py       # Feedback system
│   └── user_profile.py   # User preferences
├── templates/
│   ├── base.txt          # Basic template
│   ├── cot.txt           # Chain-of-thought
│   ├── decompose.txt     # Task decomposition
│   └── criticize.txt     # Self-criticism
└── tests/                # Test scripts
```

---

## Installation

```bash
# Via ClawHub
clawhub install promptbuddy

# Or clone from GitHub
git clone https://github.com/promptbuddy/promptbuddy.git
cd promptbuddy
```

---

## Requirements

- Python 3.12+
- numpy
- (Optional) sklearn

---

## API

```python
from smart_engine import PromptEngineer

# Initialize
engine = PromptEngineer(user_id="default")

# Process input
result = engine.process("How do rockets work?")

# Result
{
    "intent": "reasoning",
    "template": "cot",
    "confidence": 0.40,
    "optimized_prompt": "...",
    "action": "auto_output"
}
```

---

## Roadmap

| Version | Features | ETA |
|---------|----------|-----|
| v2.3 | English support, Performance optimization | 1 month |
| v2.4 | Multi-turn conversation, Prompt variants | 2 months |
| v3.0 | Enterprise version, Team collaboration | 3-6 months |

---

## Based on "The Prompt Report"

This skill is based on the paper "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques":
- 58 text prompt techniques
- 40 multimodal prompt techniques

---

## License

MIT License

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## Contact

**Project Lead**: Pengxiang Zeng
**Developer**: Xiaohong (OpenClaw First Assistant)
**Created**: 2026-03-17

---

**PromptBuddy - Make AI Truly Understand You**
OnlyPromptBuddy