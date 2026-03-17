#!/bin/bash

# 基础测试脚本

SCRIPT="./scripts/prompt-engineer.sh"

echo "=== 测试1: 简单输入 ==="
$SCRIPT "帮我写个产品描述"

echo -e "\n=== 测试2: 数学问题 (CoT) ==="
$SCRIPT "如何计算这个复杂的数学问题？"

echo -e "\n=== 测试3: 项目计划 (分解) ==="
$SCRIPT "帮我制定一个项目实施计划"

echo -e "\n=== 测试4: 质量检查 (批评) ==="
$SCRIPT "检查这个方案的质量"

echo -e "\n=== 测试5: JSON格式输出 ==="
$SCRIPT -f json "总结这篇文章的主要观点"

echo -e "\n=== 测试6: 指定模板 ==="
$SCRIPT -t cot "分析这个商业案例"

echo "测试完成！"