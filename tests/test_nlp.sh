#!/bin/bash

# NLP增强版测试脚本

SCRIPT="./scripts/prompt-engineer.sh"

echo "=== NLP测试1: 科学问题 ==="
$SCRIPT "火箭怎么上天？"

echo -e "\n=== NLP测试2: 自然现象 ==="
$SCRIPT "为什么天空是蓝色的？"

echo -e "\n=== NLP测试3: 复杂项目 ==="
$SCRIPT "如何从零开始建立一个AI创业公司？"

echo -e "\n=== NLP测试4: 简单查询 ==="
$SCRIPT "今天天气怎么样？"

echo -e "\n=== NLP测试5: 质量检查 ==="
$SCRIPT "检查这个代码的质量"

echo -e "\n=== 基础测试6: 数学问题 ==="
$SCRIPT "如何计算这个复杂的数学问题？"

echo -e "\n=== 基础测试7: 项目计划 ==="
$SCRIPT "帮我制定一个项目实施计划"

echo -e "\n=== JSON输出测试 ==="
$SCRIPT -f json "总结这篇文章的主要观点"

echo "NLP增强版测试完成！"