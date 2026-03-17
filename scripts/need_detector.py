#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Need Detection Engine for Prompt Engineering
判断用户输入是否需要 Prompt 优化
"""

import re
import json
from typing import Dict, Tuple, Optional, List


class NeedDetector:
    """需求识别引擎 - 判断用户输入是否需要 prompt 优化"""
    
    def __init__(self):
        # 任务型关键词（需要优化）
        self.task_indicators = [
            # 中文任务词
            '帮我', '请', '写一个', '写一篇', '生成', '创建', '设计',
            '解释', '分析', '总结', '翻译', '优化', '改进', '提升',
            '制定', '规划', '构建', '开发', '实现', '解决',
            '给我', '为我', '替我', '我想', '我要', '需要',
            '检查', '审核', '评估', '审查', '验证', '测试', '诊断',
            '对比', '比较', '研究', '探讨', '说明', '描述',
            # 英文任务词
            'write', 'create', 'generate', 'explain', 'analyze', 
            'help', 'please', 'design', 'build', 'develop', 'check'
        ]
        
        # 问句模式（可能需要优化）
        self.question_patterns = [
            r'如何.*', r'怎么.*', r'为什么.*', r'什么是.*',
            r'怎样.*', r'哪些.*', r'有什么.*', r'能否.*',
            r'可以.*吗', r'怎么才能.*', r'如何才能.*',
            r'请.*', r'帮.*', r'帮我.*'
        ]
        
        # 排除模式（不需要优化 - 简单查询）
        self.skip_patterns = [
            # 天气查询
            r'今天.*天气', r'明天.*天气', r'天气怎么样',
            # 简单问候
            r'^你好', r'^在吗', r'^谢谢', r'^好的', r'^ok', r'^hi', r'^hello',
            # 简单确认
            r'^是$', r'^否$', r'^对$', r'^不$',
            # 时间查询
            r'几点', r'现在.*时间', r'今天.*日期',
            # 简单数学
            r'^\d+[\+\-\*\/]\d+$'
        ]
        
        # 复杂度指标（更可能需要优化）
        self.complexity_indicators = [
            '详细', '具体', '完整', '全面', '深入', '专业',
            '步骤', '流程', '方案', '策略', '计划', '指南',
            '包括', '包含', '涉及', '相关'
        ]
    
    def detect(self, text: str) -> Dict:
        """
        判断用户输入是否需要 prompt 优化
        
        Returns:
            {
                "need_optimization": bool,  # 是否需要优化
                "confidence": float,        # 置信度 0-1
                "reason": str,              # 判断理由
                "signals": dict             # 各信号得分
            }
        """
        text = text.strip()
        signals = {
            "task_score": 0.0,
            "question_score": 0.0,
            "complexity_score": 0.0,
            "skip_score": 0.0
        }
        
        # 1. 检查排除模式（优先级最高）
        for pattern in self.skip_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return {
                    "need_optimization": False,
                    "confidence": 0.9,
                    "reason": f"匹配排除模式: {pattern}",
                    "signals": signals
                }
        
        # 2. 检测任务型需求
        task_matches = []
        for indicator in self.task_indicators:
            if indicator in text.lower():
                signals["task_score"] += 0.25
                task_matches.append(indicator)
        signals["task_score"] = min(signals["task_score"], 0.8)
        
        # 3. 检测问句模式
        question_matches = []
        for pattern in self.question_patterns:
            if re.search(pattern, text):
                signals["question_score"] += 0.3
                question_matches.append(pattern)
        signals["question_score"] = min(signals["question_score"], 0.6)
        
        # 4. 检测复杂度指标
        complexity_matches = []
        for indicator in self.complexity_indicators:
            if indicator in text:
                signals["complexity_score"] += 0.15
                complexity_matches.append(indicator)
        signals["complexity_score"] = min(signals["complexity_score"], 0.5)
        
        # 5. 计算综合得分
        # 加权计算：任务词权重最高
        total_score = (
            signals["task_score"] * 0.7 +
            signals["question_score"] * 0.2 +
            signals["complexity_score"] * 0.1
        )
        
        # 如果有任何任务词或问句模式，确保最低分数
        if signals["task_score"] > 0 or signals["question_score"] > 0:
            total_score = max(total_score, 0.25)
        
        # 6. 文本长度加分（长文本更可能需要优化）
        word_count = len(text.split())
        if word_count > 20:
            total_score += 0.1
        elif word_count > 10:
            total_score += 0.05
        
        # 7. 最终判断
        total_score = min(total_score, 0.95)
        
        # 阈值判断
        THRESHOLD = 0.20  # 需求识别阈值（降低以更激进）
        
        need_optimization = total_score >= THRESHOLD
        
        # 构建理由
        reasons = []
        if task_matches:
            reasons.append(f"任务词: {', '.join(task_matches[:3])}")
        if question_matches:
            reasons.append(f"问句模式: {len(question_matches)}个")
        if complexity_matches:
            reasons.append(f"复杂度: {', '.join(complexity_matches[:3])}")
        
        reason = " | ".join(reasons) if reasons else "无明显优化需求特征"
        
        return {
            "need_optimization": need_optimization,
            "confidence": round(total_score, 2),
            "reason": reason,
            "signals": signals
        }


class AutoDecisionEngine:
    """自动决策引擎 - 综合判断并做出决策"""
    
    # 置信度阈值（高于此值直接输出，低于此值询问确认）
    # 设为 0.20 更激进，让系统更自动
    CONFIDENCE_THRESHOLD = 0.20
    
    def __init__(self):
        self.need_detector = NeedDetector()
    
    def decide(self, text: str, intent_result: dict, user_profile: dict = None) -> Dict:
        """
        综合决策
        
        Args:
            text: 用户输入
            intent_result: 意图识别结果（来自 multi_model_engine）
            user_profile: 用户偏好配置
        
        Returns:
            {
                "action": "auto_output" | "ask_confirm" | "skip",
                "template": str,           # 推荐模板
                "confidence": float,       # 最终置信度
                "reason": str,             # 决策理由
                "alternatives": list       # 备选模板（如果需要确认）
            }
        """
        # 1. 需求识别
        need_result = self.need_detector.detect(text)
        
        if not need_result["need_optimization"]:
            return {
                "action": "skip",
                "template": None,
                "confidence": need_result["confidence"],
                "reason": f"不需要优化: {need_result['reason']}",
                "alternatives": []
            }
        
        # 2. 获取意图
        intent = intent_result.get("best_intent", "simple")
        intent_confidence = intent_result.get("confidence", 0)
        
        # 3. 结合用户偏好
        preferred_template = None
        if user_profile:
            preferred_template = user_profile.get("preferred_template")
        
        # 4. 选择模板
        template_mapping = {
            "reasoning": "cot",
            "decomposition": "decompose",
            "criticism": "criticize",
            "simple": "base"
        }
        
        # 如果用户有偏好且意图不是特别明确，倾向用户偏好
        if preferred_template and intent_confidence < 0.5:
            selected_template = preferred_template
        else:
            selected_template = template_mapping.get(intent, "base")
        
        # 5. 计算最终置信度
        # 综合需求置信度和意图置信度
        final_confidence = (
            need_result["confidence"] * 0.4 +
            intent_confidence * 0.6
        )
        
        # 6. 决策
        # 动态阈值：如果有用户偏好且一致，降低阈值
        threshold = self.CONFIDENCE_THRESHOLD
        if preferred_template and preferred_template == selected_template:
            threshold -= 0.1  # 用户偏好一致，更信任
        
        if final_confidence >= threshold:
            # 高置信度：自动输出
            return {
                "action": "auto_output",
                "template": selected_template,
                "confidence": round(final_confidence, 2),
                "reason": f"置信度 {final_confidence:.2f} ≥ {threshold:.2f}，自动选择 {selected_template}",
                "alternatives": []
            }
        else:
            # 低置信度：询问确认
            alternatives = self._get_alternatives(selected_template, intent)
            return {
                "action": "ask_confirm",
                "template": selected_template,
                "confidence": round(final_confidence, 2),
                "reason": f"置信度 {final_confidence:.2f} < {threshold:.2f}，建议确认",
                "alternatives": alternatives
            }
    
    def _get_alternatives(self, primary: str, intent: str) -> List[Dict]:
        """获取备选模板"""
        all_templates = [
            {"name": "base", "desc": "基础模板 - 通用回答"},
            {"name": "cot", "desc": "思维链 - 逐步推理"},
            {"name": "decompose", "desc": "任务分解 - 分步骤指南"},
            {"name": "criticize", "desc": "自我批评 - 质量检查"}
        ]
        
        # 排除已选的，返回其他选项
        return [t for t in all_templates if t["name"] != primary]


def main():
    """测试入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 need_detector.py \"user input\"")
        sys.exit(1)
    
    input_text = sys.argv[1]
    
    # 需求识别
    detector = NeedDetector()
    result = detector.detect(input_text)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()