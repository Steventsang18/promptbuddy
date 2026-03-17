#!/bin/bash

# PromptBuddy - 智能Prompt工程自动化
# v2.0 - 集成需求识别 + 意图识别 + 用户偏好学习
# 使用 Python 智能引擎

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SMART_ENGINE="$SCRIPT_DIR/smart_engine.py"

# 显示帮助
show_help() {
    cat << EOF
PromptBuddy v2.0 - 智能 Prompt 工程自动化

用法:
  $0 "用户输入"                    # 自动识别，直接输出
  $0 -t cot "火箭如何上天？"       # 强制使用思维链模板
  $0 -f json "帮我写个产品描述"    # JSON格式输出
  $0 --stats                       # 查看用户偏好统计
  $0 --recent                      # 查看最近查询历史

模板类型:
  auto       自动选择（默认）
  base       基础模板 - 通用回答
  cot        思维链 - 逐步推理
  decompose  任务分解 - 分步骤指南
  criticize  自我批评 - 质量检查

示例:
  $0 "帮我优化这个prompt"
  $0 "火箭如何上天？"
  $0 "如何从零开始创建一个项目？"
  $0 -t decompose "建立一套完整的工作流程"

功能亮点:
  ✅ 自动判断是否需要优化
  ✅ 智能选择最佳模板
  ✅ 学习用户偏好
  ✅ 高置信度直接输出，低置信度提供备选
EOF
}

# 解析参数
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# 调用智能引擎
python3 "$SMART_ENGINE" "$@"