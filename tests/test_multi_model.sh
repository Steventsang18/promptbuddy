#!/bin/bash

# 多模型语义引擎综合测试

SCRIPT="./scripts/prompt-engineer.sh"

echo "=== 多模型测试1: 科学问题 ==="
$SCRIPT "火箭怎么上天？"

echo -e "\n=== 多模型测试2: 技术算法 ==="
$SCRIPT "如何设计一个高效的机器学习算法？"

echo -e "\n=== 多模型测试3: AI创业 ==="
$SCRIPT "如何从零开始建立一个AI创业公司？"

echo -e "\n=== 多模型测试4: 简单查询 ==="
$SCRIPT "今天天气怎么样？"

echo -e "\n=== 多模型测试5: 质量检查 ==="
$SCRIPT "检查这个深度学习模型的代码质量"

echo -e "\n=== 多模型测试6: 学术研究 ==="
$SCRIPT "分析量子计算对密码学的影响"

echo -e "\n=== 多模型测试7: 商业策略 ==="
$SCRIPT "制定一个完整的数字营销策略方案"

echo -e "\n=== JSON输出测试 ==="
$SCRIPT -f json "总结这篇关于AI伦理的论文"

echo "多模型语义引擎综合测试完成！"