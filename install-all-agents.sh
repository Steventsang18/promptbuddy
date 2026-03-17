#!/bin/bash
# PromptBuddy 全局安装脚本
# 确保所有 Agent 都安装并启用 PromptBuddy

echo "=== PromptBuddy 全局安装检查 ==="
echo ""

SOURCE=~/.openclaw/workspace/skills/promptbuddy
AGENTS="workspace workspace_sunny workspace_xiaohong workspace_xiaowu workspace_xiaoxin"

for ws in $AGENTS; do
    TARGET=~/.openclaw/$ws/skills/promptbuddy
    
    if [ -d "$TARGET" ] && [ -f "$TARGET/SKILL.md" ]; then
        echo "✅ $ws: 已安装"
    else
        echo "📦 $ws: 正在安装..."
        mkdir -p ~/.openclaw/$ws/skills
        cp -r "$SOURCE" "$TARGET"
        echo "✅ $ws: 安装完成"
    fi
done

echo ""
echo "=== 验证安装 ==="
for ws in $AGENTS; do
    SKILL_FILE=~/.openclaw/$ws/skills/promptbuddy/SKILL.md
    if [ -f "$SKILL_FILE" ]; then
        name=$(grep "^name:" "$SKILL_FILE" | head -1 | awk '{print $2}')
        echo "✅ $ws: $name"
    else
        echo "❌ $ws: 未找到"
    fi
done

echo ""
echo "=== 同步 AGENTS.md ==="
for ws in workspace_sunny workspace_xiaohong workspace_xiaowu workspace_xiaoxin; do
    cp ~/.openclaw/workspace/AGENTS.md ~/.openclaw/$ws/AGENTS.md 2>/dev/null
done
echo "✅ 已同步 AGENTS.md 到所有 workspace"

echo ""
echo "✅ PromptBuddy 已安装到所有 Agent"
echo ""
echo "⚠️  重要提示："
echo "  1. 对于已存在的会话，需要新建对话才能生效"
echo "  2. 或者在对话中问：'你安装了 promptbuddy 技能吗？请激活使用'"
echo "  3. 新会话会自动加载 PromptBuddy"