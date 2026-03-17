#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prompt Engineer - 智能Prompt工程自动化主引擎
v2.2 - 集成需求识别、语义意图识别、用户偏好学习、混合反馈系统
"""

import sys
import os
import json
import argparse
from datetime import datetime

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from need_detector import NeedDetector, AutoDecisionEngine
from multi_model_engine import MultiModelEngine
from user_profile import UserProfileManager
from feedback import (
    FeedbackCollector, 
    FeedbackTrigger, 
    ImplicitFeedbackDetector,
    AdaptiveDecisionMaker
)
from semantic_engine import SemanticEngine, HybridIntentDetector


class PromptEngineer:
    """Prompt工程主引擎"""
    
    TEMPLATES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "templates")
    
    def __init__(self, user_id: str = "default"):
        # 核心引擎
        self.need_detector = NeedDetector()
        self.decision_engine = AutoDecisionEngine()
        self.intent_engine = MultiModelEngine()
        self.user_profile = UserProfileManager(user_id)
        
        # 语义引擎（新增）
        self.semantic_engine = SemanticEngine()
        self.hybrid_detector = HybridIntentDetector(self.semantic_engine)
        
        # 反馈系统
        self.feedback_collector = FeedbackCollector(user_id)
        self.feedback_trigger = FeedbackTrigger()
        self.implicit_detector = ImplicitFeedbackDetector()
        self.adaptive_decision = AdaptiveDecisionMaker(self.feedback_collector)
    
    def load_template(self, template_name: str) -> str:
        """加载模板内容"""
        name_mapping = {
            "cot": "cot",
            "decompose": "decompose", 
            "criticize": "criticize",
            "base": "base"
        }
        
        actual_name = name_mapping.get(template_name, "base")
        template_path = os.path.join(self.TEMPLATES_DIR, f"{actual_name}.txt")
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """获取默认模板"""
        return """[角色设定] 你是一位专业的助手
[指令] {input}
[要求]
- 提供清晰、准确的回答
- 保持专业和友好的语调
[输出格式] 简洁明了的文本回答"""
    
    def generate_prompt(self, user_input: str, template_name: str) -> str:
        """生成优化后的Prompt"""
        template = self.load_template(template_name)
        return template.replace("{input}", user_input)
    
    def process(self, user_input: str, 
                force_template: str = None, 
                output_format: str = "text") -> dict:
        """
        处理用户输入，返回优化结果
        
        集成了渐进式智能反馈：
        - 新用户（<5次）：保守策略，低置信度时确认
        - 学习期（5-20次）：中等策略
        - 成熟期（>20次）：激进策略，几乎自动
        """
        result = {
            "original_input": user_input,
            "timestamp": datetime.now().isoformat(),
            "need_optimization": None,
            "intent": None,
            "template": None,
            "optimized_prompt": None,
            "action": None,
            "confidence": 0,
            "reason": None,
            "alternatives": [],
            "feedback_required": False,
            "feedback_style": None,
            "user_phase": "new_user"
        }
        
        # 获取用户阶段
        total_uses = self.user_profile.profile["stats"]["total_optimizations"]
        result["user_phase"] = self.feedback_trigger.get_phase(total_uses)
        
        # 1. 如果强制指定模板
        if force_template and force_template != "auto":
            result["template"] = force_template
            result["action"] = "forced"
            result["reason"] = f"用户指定模板: {force_template}"
            result["optimized_prompt"] = self.generate_prompt(user_input, force_template)
            
            self.user_profile.record_query(
                query=user_input,
                intent="unknown",
                template=force_template,
                action_taken="manual_select",
                user_feedback="accepted"
            )
            return result
        
        # 2. 需求识别
        need_result = self.need_detector.detect(user_input)
        result["need_optimization"] = need_result["need_optimization"]
        
        if not need_result["need_optimization"]:
            result["action"] = "skip"
            result["reason"] = need_result["reason"]
            result["confidence"] = need_result["confidence"]
            return result
        
        # 3. 意图识别（使用混合检测器）
        # 先获取关键词结果
        keyword_intent_result = self.intent_engine.ensemble_analyze(user_input)
        keyword_result = {
            "intent": keyword_intent_result["best_intent"],
            "confidence": keyword_intent_result["confidence"]
        }
        
        # 使用混合检测器融合语义和关键词
        hybrid_result = self.hybrid_detector.detect(
            user_input,
            keyword_result=keyword_result,
            use_fusion=True
        )
        
        result["intent"] = hybrid_result["intent"]
        result["intent_method"] = hybrid_result["method"]  # 记录使用的方法
        
        # 构建融合后的意图结果
        intent_result = {
            "best_intent": hybrid_result["intent"],
            "confidence": hybrid_result["confidence"]
        }
        
        # 4. 获取自适应阈值
        adaptive_threshold = self.adaptive_decision.get_adaptive_threshold(total_uses)
        
        # 5. 自动决策（结合用户偏好和自适应阈值）
        user_pref = {
            "preferred_template": self.user_profile.get_preferred_template(),
            "auto_threshold": adaptive_threshold
        }
        
        decision = self.decision_engine.decide(
            user_input, 
            intent_result, 
            user_pref
        )
        
        # 6. 检查是否需要根据历史反馈调整
        adjustment = self.adaptive_decision.should_adjust_template(
            decision["template"],
            decision["confidence"]
        )
        
        if adjustment["adjust"]:
            result["template"] = adjustment["alternative"]
            result["reason"] = f"已调整: {adjustment['reason']}"
        else:
            result["template"] = decision["template"]
            result["reason"] = decision["reason"]
        
        result["action"] = decision["action"]
        result["confidence"] = decision["confidence"]
        result["alternatives"] = decision.get("alternatives", [])
        
        # 7. 判断是否需要反馈确认（渐进式）
        should_ask, feedback_style = self.feedback_trigger.should_ask_feedback(
            decision["confidence"],
            total_uses
        )
        
        result["feedback_required"] = should_ask
        result["feedback_style"] = feedback_style
        
        # 8. 生成优化后的Prompt
        if decision["action"] in ["auto_output", "ask_confirm"]:
            result["optimized_prompt"] = self.generate_prompt(
                user_input, 
                result["template"]
            )
        
        # 9. 记录使用
        if decision["action"] == "auto_output":
            self.user_profile.record_query(
                query=user_input,
                intent=result["intent"],
                template=result["template"],
                action_taken="auto_output",
                user_feedback="accepted"
            )
        
        return result
    
    def record_feedback(self, 
                       query: str,
                       template: str,
                       feedback_type: str,
                       confidence: float,
                       new_template: str = None):
        """记录用户反馈"""
        self.feedback_collector.record_explicit(
            query=query,
            template=template,
            feedback_type=feedback_type,
            confidence=confidence,
            new_template=new_template
        )
    
    def detect_implicit_feedback(self, user_message: str) -> dict:
        """检测隐式反馈"""
        return self.implicit_detector.analyze_message(user_message)
    
    def format_output(self, result: dict, output_format: str = "text") -> str:
        """格式化输出"""
        if output_format == "json":
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        lines = []
        
        if result["action"] == "skip":
            lines.append(f"⚠️  跳过优化: {result['reason']}")
            return "\n".join(lines)
        
        # 阶段标识
        phase_icons = {
            "new_user": "🆕 新用户",
            "learning": "📈 学习中",
            "mature": "⭐ 成熟"
        }
        phase_label = phase_icons.get(result["user_phase"], "")
        
        lines.append("=" * 50)
        lines.append(f"📊 分析结果 {phase_label}")
        lines.append("-" * 50)
        lines.append(f"意图: {result['intent']}")
        lines.append(f"模板: {result['template']}")
        lines.append(f"置信度: {result['confidence']:.2f}")
        lines.append(f"决策: {result['action']}")
        if result.get("reason"):
            lines.append(f"理由: {result['reason']}")
        lines.append("=" * 50)
        lines.append("")
        lines.append("📝 优化后的 Prompt")
        lines.append("-" * 50)
        lines.append(result["optimized_prompt"])
        
        # 反馈提示（如果需要）
        if result.get("feedback_required"):
            lines.append("")
            lines.append("─" * 50)
            
            style = result.get("feedback_style", "quick")
            if style == "confirm":
                lines.append("👍 很好  |  🔄 换一个  |  ❌ 不需要")
            elif style == "quick":
                lines.append("👍 接受  |  🔄 换模板")
            else:  # suggest
                lines.append("💡 这是推荐的模板，觉得合适吗？ 👍/🔄")
        
        # 备选项
        if result["action"] == "ask_confirm" and result.get("alternatives"):
            lines.append("")
            lines.append("🔄 备选模板:")
            for alt in result["alternatives"]:
                lines.append(f"  - {alt['name']}: {alt['desc']}")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="智能Prompt工程自动化 v2.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "帮我写个产品描述"           # 自动处理
  %(prog)s -t cot "火箭如何上天？"      # 强制使用CoT模板
  %(prog)s --stats                      # 查看用户统计
  %(prog)s --feedback-stats             # 查看反馈统计
  %(prog)s --test-trigger               # 测试反馈触发逻辑
        """
    )
    parser.add_argument("input", nargs="?", help="用户输入")
    parser.add_argument("-t", "--template", default="auto",
                        choices=["auto", "base", "cot", "decompose", "criticize"],
                        help="模板类型 (默认: auto)")
    parser.add_argument("-f", "--format", default="text",
                        choices=["text", "json"],
                        help="输出格式 (默认: text)")
    parser.add_argument("-u", "--user", default="default",
                        help="用户ID (用于偏好学习)")
    parser.add_argument("--stats", action="store_true",
                        help="显示用户使用统计")
    parser.add_argument("--feedback-stats", action="store_true",
                        help="显示反馈统计")
    parser.add_argument("--recent", action="store_true",
                        help="显示最近查询")
    parser.add_argument("--test-trigger", action="store_true",
                        help="测试反馈触发逻辑")
    
    args = parser.parse_args()
    
    engine = PromptEngineer(user_id=args.user)
    
    # 显示用户统计
    if args.stats:
        stats = engine.user_profile.get_stats_summary()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
    
    # 显示反馈统计
    if args.feedback_stats:
        stats = engine.feedback_collector.get_stats_summary()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
    
    # 显示最近查询
    if args.recent:
        recent = engine.user_profile.get_recent_queries()
        print(json.dumps(recent, ensure_ascii=False, indent=2))
        return
    
    # 测试反馈触发
    if args.test_trigger:
        print("📊 反馈触发测试")
        print("=" * 50)
        for uses in [2, 10, 25]:
            print(f"\n用户阶段: {engine.feedback_trigger.get_phase(uses)} (使用次数: {uses})")
            for conf in [0.15, 0.25, 0.35]:
                ask, style = engine.feedback_trigger.should_ask_feedback(conf, uses)
                print(f"  置信度 {conf:.2f} → 询问={ask}, 风格={style}")
        return
    
    # 处理输入
    if not args.input:
        parser.print_help()
        sys.exit(1)
    
    result = engine.process(
        user_input=args.input,
        force_template=args.template,
        output_format=args.format
    )
    
    print(engine.format_output(result, args.format))


if __name__ == "__main__":
    main()