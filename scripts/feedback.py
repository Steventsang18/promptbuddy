#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Feedback System for Prompt Engineering
混合 + 渐进式智能反馈系统
"""

import json
import os
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class FeedbackType(Enum):
    """反馈类型"""
    ACCEPTED = "accepted"           # 用户接受了输出
    CHANGED = "changed"             # 用户换了模板
    REJECTED = "rejected"           # 用户拒绝了
    USED_OUTPUT = "used_output"     # 隐式：用户使用了输出
    FOLLOW_UP = "follow_up"         # 隐式：用户追问
    IGNORED = "ignored"             # 隐式：用户忽略


class FeedbackTrigger:
    """反馈触发器 - 决定何时询问用户"""
    
    # 不同阶段的阈值
    NEW_USER_THRESHOLD = 0.35        # 新用户阈值（较保守）
    LEARNING_THRESHOLD = 0.25       # 学习期阈值
    MATURE_THRESHOLD = 0.15         # 成熟期阈值
    
    # 阶段划分
    NEW_USER_LIMIT = 5              # 新用户：0-5次
    LEARNING_LIMIT = 20             # 学习期：6-20次
    
    def should_ask_feedback(self, 
                           confidence: float,
                           total_uses: int) -> Tuple[bool, str]:
        """
        判断是否需要询问用户反馈
        
        Returns:
            (should_ask, feedback_style)
            feedback_style: "confirm" | "quick" | "suggest" | None
        """
        # 新用户：保守策略
        if total_uses < self.NEW_USER_LIMIT:
            if confidence < self.NEW_USER_THRESHOLD:
                return True, "confirm"
            return False, None
        
        # 学习期：中等策略
        elif total_uses < self.LEARNING_LIMIT:
            if confidence < self.LEARNING_THRESHOLD:
                return True, "quick"
            return False, None
        
        # 成熟期：激进策略
        else:
            if confidence < self.MATURE_THRESHOLD:
                return True, "suggest"
            return False, None
        
        return False, None
    
    def get_phase(self, total_uses: int) -> str:
        """获取用户阶段"""
        if total_uses < self.NEW_USER_LIMIT:
            return "new_user"
        elif total_uses < self.LEARNING_LIMIT:
            return "learning"
        else:
            return "mature"


class ImplicitFeedbackDetector:
    """隐式反馈检测器 - 观察用户行为"""
    
    def __init__(self):
        self.session_outputs = {}  # 记录本次会话的输出
    
    def register_output(self, query: str, output: str, template: str) -> str:
        """注册输出，返回输出ID"""
        output_id = self._generate_id(query)
        self.session_outputs[output_id] = {
            "query": query,
            "output": output,
            "template": template,
            "timestamp": time.time(),
            "used": False,
            "follow_ups": 0
        }
        return output_id
    
    def detect_usage(self, user_message: str, output_id: str = None) -> Optional[str]:
        """
        检测用户是否使用了输出
        
        Returns:
            FeedbackType or None
        """
        # 检查是否基于输出继续对话（追问）
        follow_up_indicators = [
            "还有", "另外", "那", "接着", "继续",
            "更详细", "具体", "举个例子", "为什么"
        ]
        
        for indicator in follow_up_indicators:
            if indicator in user_message:
                return FeedbackType.FOLLOW_UP.value
        
        return None
    
    def detect_rejection(self, user_message: str) -> Optional[str]:
        """检测用户是否拒绝了输出"""
        rejection_indicators = [
            "不要这个", "不对", "不是这个意思",
            "换一个", "重新", "算了", "跳过"
        ]
        
        for indicator in rejection_indicators:
            if indicator in user_message:
                return FeedbackType.REJECTED.value
        
        return None
    
    def detect_change_request(self, user_message: str) -> Optional[str]:
        """检测用户是否想换模板"""
        change_indicators = [
            "换个", "换一个", "用另一个", "试试其他",
            "换个模板", "换个方式"
        ]
        
        for indicator in change_indicators:
            if indicator in user_message:
                return FeedbackType.CHANGED.value
        
        return None
    
    def analyze_message(self, 
                       user_message: str,
                       output_id: str = None) -> Dict:
        """
        分析用户消息，判断隐式反馈
        
        Returns:
            {
                "feedback_type": str or None,
                "detected": bool,
                "signals": list
            }
        """
        signals = []
        feedback_type = None
        
        # 1. 检测拒绝
        rejected = self.detect_rejection(user_message)
        if rejected:
            feedback_type = rejected
            signals.append("rejection_detected")
        
        # 2. 检测换模板请求
        changed = self.detect_change_request(user_message)
        if changed:
            feedback_type = changed
            signals.append("change_requested")
        
        # 3. 检测追问（优先级最低）
        if not feedback_type:
            follow_up = self.detect_usage(user_message, output_id)
            if follow_up:
                feedback_type = follow_up
                signals.append("follow_up_detected")
        
        return {
            "feedback_type": feedback_type,
            "detected": feedback_type is not None,
            "signals": signals
        }
    
    def _generate_id(self, query: str) -> str:
        """生成输出ID"""
        return hashlib.md5(
            f"{query}_{time.time()}".encode()
        ).hexdigest()[:8]


class FeedbackCollector:
    """反馈收集器 - 统一收集和管理反馈"""
    
    def __init__(self, user_id: str = "default", 
                 storage_dir: str = None):
        self.user_id = user_id
        self.storage_dir = storage_dir or os.path.expanduser(
            "~/.openclaw/workspace/skills/prompt-engineer/feedback"
        )
        self.feedback_file = os.path.join(
            self.storage_dir, f"feedback_{user_id}.json"
        )
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self) -> Dict:
        """加载反馈数据"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "feedbacks": [],
            "stats": {
                "total": 0,
                "accepted": 0,
                "changed": 0,
                "rejected": 0,
                "implicit": 0
            },
            "template_stats": {
                "base": {"used": 0, "accepted": 0, "changed_from": 0},
                "cot": {"used": 0, "accepted": 0, "changed_from": 0},
                "decompose": {"used": 0, "accepted": 0, "changed_from": 0},
                "criticize": {"used": 0, "accepted": 0, "changed_from": 0}
            }
        }
    
    def _save_feedback(self):
        """保存反馈数据"""
        os.makedirs(self.storage_dir, exist_ok=True)
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def record_explicit(self,
                       query: str,
                       template: str,
                       feedback_type: str,
                       confidence: float,
                       new_template: str = None):
        """
        记录显式反馈
        
        Args:
            query: 用户原始输入
            template: 使用的模板
            feedback_type: accepted/changed/rejected
            confidence: 置信度
            new_template: 如果changed，新模板是什么
        """
        feedback_entry = {
            "id": hashlib.md5(f"{query}_{time.time()}".encode()).hexdigest()[:8],
            "timestamp": datetime.now().isoformat(),
            "type": "explicit",
            "feedback_type": feedback_type,
            "query": query[:100],
            "template": template,
            "new_template": new_template,
            "confidence": confidence
        }
        
        self._add_feedback(feedback_entry, template, feedback_type, new_template)
    
    def record_implicit(self,
                       query: str,
                       template: str,
                       detected_type: str,
                       confidence: float):
        """
        记录隐式反馈
        """
        feedback_entry = {
            "id": hashlib.md5(f"{query}_{time.time()}".encode()).hexdigest()[:8],
            "timestamp": datetime.now().isoformat(),
            "type": "implicit",
            "feedback_type": detected_type,
            "query": query[:100],
            "template": template,
            "confidence": confidence
        }
        
        self._add_feedback(feedback_entry, template, detected_type)
    
    def _add_feedback(self, 
                     entry: dict, 
                     template: str,
                     feedback_type: str,
                     new_template: str = None):
        """添加反馈记录并更新统计"""
        # 添加记录
        self.feedback_data["feedbacks"].append(entry)
        self.feedback_data["stats"]["total"] += 1
        
        # 更新总统计
        if feedback_type == FeedbackType.ACCEPTED.value:
            self.feedback_data["stats"]["accepted"] += 1
        elif feedback_type == FeedbackType.CHANGED.value:
            self.feedback_data["stats"]["changed"] += 1
        elif feedback_type == FeedbackType.REJECTED.value:
            self.feedback_data["stats"]["rejected"] += 1
        elif feedback_type in [FeedbackType.USED_OUTPUT.value, 
                               FeedbackType.FOLLOW_UP.value]:
            self.feedback_data["stats"]["implicit"] += 1
            # 隐式正面反馈也计入接受
            self.feedback_data["stats"]["accepted"] += 1
        
        # 更新模板统计
        if template in self.feedback_data["template_stats"]:
            self.feedback_data["template_stats"][template]["used"] += 1
            if feedback_type in [FeedbackType.ACCEPTED.value,
                                FeedbackType.USED_OUTPUT.value,
                                FeedbackType.FOLLOW_UP.value]:
                self.feedback_data["template_stats"][template]["accepted"] += 1
            elif feedback_type == FeedbackType.CHANGED.value:
                self.feedback_data["template_stats"][template]["changed_from"] += 1
        
        # 如果换到了新模板，更新新模板的统计
        if new_template and new_template in self.feedback_data["template_stats"]:
            self.feedback_data["template_stats"][new_template]["accepted"] += 1
        
        self._save_feedback()
    
    def get_acceptance_rate(self, template: str = None) -> float:
        """获取接受率"""
        stats = self.feedback_data["stats"]
        
        if stats["total"] == 0:
            return 0.0
        
        if template:
            t_stats = self.feedback_data["template_stats"].get(template, {})
            if t_stats.get("used", 0) == 0:
                return 0.0
            return t_stats.get("accepted", 0) / t_stats["used"]
        
        # 总体接受率
        total = stats["total"]
        accepted = stats["accepted"]
        return accepted / total
    
    def get_template_rejection_rate(self, template: str) -> float:
        """获取某模板的拒绝/更换率"""
        t_stats = self.feedback_data["template_stats"].get(template, {})
        used = t_stats.get("used", 0)
        if used == 0:
            return 0.0
        
        changed = t_stats.get("changed_from", 0)
        return changed / used
    
    def get_stats_summary(self) -> Dict:
        """获取统计摘要"""
        stats = self.feedback_data["stats"]
        template_stats = self.feedback_data["template_stats"]
        
        return {
            "total_feedbacks": stats["total"],
            "explicit_feedbacks": stats["accepted"] + stats["changed"] + stats["rejected"],
            "implicit_feedbacks": stats["implicit"],
            "overall_acceptance_rate": self.get_acceptance_rate(),
            "template_performance": {
                t: {
                    "used": s["used"],
                    "acceptance_rate": s["accepted"] / max(s["used"], 1),
                    "rejection_rate": s["changed_from"] / max(s["used"], 1)
                }
                for t, s in template_stats.items()
                if s["used"] > 0
            }
        }


class AdaptiveDecisionMaker:
    """自适应决策器 - 根据反馈调整决策"""
    
    def __init__(self, feedback_collector: FeedbackCollector):
        self.feedback = feedback_collector
    
    def should_adjust_template(self, 
                               suggested_template: str,
                               confidence: float) -> Dict:
        """
        判断是否需要调整模板
        
        Returns:
            {
                "adjust": bool,
                "reason": str,
                "alternative": str or None
            }
        """
        # 获取该模板的拒绝率
        rejection_rate = self.feedback.get_template_rejection_rate(suggested_template)
        
        # 如果拒绝率很高，考虑调整
        if rejection_rate > 0.6:
            alternative = self._find_better_template(suggested_template)
            return {
                "adjust": True,
                "reason": f"模板 {suggested_template} 历史拒绝率较高 ({rejection_rate:.0%})",
                "alternative": alternative
            }
        
        return {
            "adjust": False,
            "reason": None,
            "alternative": None
        }
    
    def get_adaptive_threshold(self, total_uses: int) -> float:
        """获取自适应阈值"""
        acceptance_rate = self.feedback.get_acceptance_rate()
        
        base_threshold = 0.20
        
        # 根据接受率动态调整
        if total_uses < 10:
            # 样本不足，保守
            return 0.30
        elif acceptance_rate > 0.8:
            # 接受率高，可以更激进
            return max(0.15, base_threshold - 0.05)
        elif acceptance_rate < 0.5:
            # 接受率低，更保守
            return min(0.35, base_threshold + 0.10)
        else:
            return base_threshold
    
    def _find_better_template(self, avoid_template: str) -> str:
        """找到更好的替代模板"""
        template_stats = self.feedback.feedback_data["template_stats"]
        
        best_template = None
        best_rate = 0
        
        for template, stats in template_stats.items():
            if template == avoid_template:
                continue
            if stats["used"] < 3:
                continue  # 样本太少
            
            rate = stats["accepted"] / max(stats["used"], 1)
            if rate > best_rate:
                best_rate = rate
                best_template = template
        
        return best_template or "base"


def main():
    """测试入口"""
    import sys
    
    collector = FeedbackCollector("test_user")
    trigger = FeedbackTrigger()
    implicit = ImplicitFeedbackDetector()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "stats":
            print(json.dumps(collector.get_stats_summary(), ensure_ascii=False, indent=2))
        
        elif cmd == "test":
            # 测试反馈触发
            for uses in [2, 10, 25]:
                for conf in [0.15, 0.25, 0.35]:
                    ask, style = trigger.should_ask_feedback(conf, uses)
                    phase = trigger.get_phase(uses)
                    print(f"uses={uses:2d}, conf={conf:.2f} → ask={ask}, style={style}, phase={phase}")
        
        elif cmd == "implicit":
            # 测试隐式检测
            test_messages = [
                "还有其他方案吗",
                "不对，不是这个意思",
                "换个模板试试",
                "继续详细说说",
                "算了跳过"
            ]
            for msg in test_messages:
                result = implicit.analyze_message(msg)
                print(f"'{msg}' → {result}")
    else:
        print("用法:")
        print("  python3 feedback.py stats     # 查看反馈统计")
        print("  python3 feedback.py test      # 测试触发逻辑")
        print("  python3 feedback.py implicit  # 测试隐式检测")


if __name__ == "__main__":
    main()