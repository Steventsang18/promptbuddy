#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User Profile Manager for Prompt Engineering
用户偏好学习和记忆系统
"""

import json
import os
from typing import Dict, Optional, List
from datetime import datetime


class UserProfileManager:
    """用户偏好管理器 - 学习和记忆用户习惯"""
    
    DEFAULT_PROFILE = {
        "user_id": None,
        "created_at": None,
        "last_updated": None,
        "stats": {
            "total_queries": 0,
            "total_optimizations": 0,
            "auto_accepted": 0,
            "manual_selected": 0
        },
        "template_usage": {
            "base": {"used": 0, "accepted": 0},
            "cot": {"used": 0, "accepted": 0},
            "decompose": {"used": 0, "accepted": 0},
            "criticize": {"used": 0, "accepted": 0}
        },
        "question_types": {
            "scientific": 0,
            "planning": 0,
            "quality": 0,
            "general": 0
        },
        "recent_queries": [],  # 最近 20 条查询
        "preferences": {
            "preferred_template": None,
            "auto_accept_threshold": 0.45,
            "verbosity": "normal"  # concise, normal, detailed
        }
    }
    
    def __init__(self, user_id: str = "default", profile_dir: str = None):
        self.user_id = user_id
        self.profile_dir = profile_dir or os.path.expanduser(
            "~/.openclaw/workspace/skills/prompt-engineer"
        )
        self.profile_path = os.path.join(self.profile_dir, f"user_profile_{user_id}.json")
        self.profile = self.load_profile()
    
    def load_profile(self) -> Dict:
        """加载用户配置"""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    # 合并默认值（处理新增字段）
                    return {**self.DEFAULT_PROFILE, **profile}
            except Exception as e:
                print(f"加载配置失败: {e}")
        
        # 创建新配置
        profile = self.DEFAULT_PROFILE.copy()
        profile["user_id"] = self.user_id
        profile["created_at"] = datetime.now().isoformat()
        profile["last_updated"] = datetime.now().isoformat()
        return profile
    
    def save_profile(self):
        """保存用户配置"""
        self.profile["last_updated"] = datetime.now().isoformat()
        
        os.makedirs(self.profile_dir, exist_ok=True)
        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)
    
    def record_query(self, query: str, intent: str, template: str, 
                     action_taken: str, user_feedback: str = None):
        """
        记录用户查询和行为
        
        Args:
            query: 用户原始输入
            intent: 识别的意图
            template: 使用的模板
            action_taken: 执行的动作 (auto_output, manual_select, skipped)
            user_feedback: 用户反馈 (accepted, changed, rejected)
        """
        # 更新统计
        self.profile["stats"]["total_queries"] += 1
        
        if action_taken in ["auto_output", "manual_select"]:
            self.profile["stats"]["total_optimizations"] += 1
        
        if action_taken == "auto_output" and user_feedback == "accepted":
            self.profile["stats"]["auto_accepted"] += 1
        elif action_taken == "manual_select":
            self.profile["stats"]["manual_selected"] += 1
        
        # 更新模板使用统计
        if template and template in self.profile["template_usage"]:
            self.profile["template_usage"][template]["used"] += 1
            if user_feedback in ["accepted", None]:
                self.profile["template_usage"][template]["accepted"] += 1
        
        # 更新问题类型统计
        intent_to_type = {
            "reasoning": "scientific",
            "decomposition": "planning",
            "criticism": "quality",
            "simple": "general"
        }
        q_type = intent_to_type.get(intent, "general")
        self.profile["question_types"][q_type] += 1
        
        # 记录最近查询
        recent = {
            "query": query[:100],  # 截断长查询
            "intent": intent,
            "template": template,
            "action": action_taken,
            "feedback": user_feedback,
            "timestamp": datetime.now().isoformat()
        }
        self.profile["recent_queries"].append(recent)
        # 只保留最近 20 条
        self.profile["recent_queries"] = self.profile["recent_queries"][-20:]
        
        # 更新偏好
        self._update_preferences()
        
        # 保存
        self.save_profile()
    
    def _update_preferences(self):
        """根据历史行为更新用户偏好"""
        stats = self.profile["stats"]
        usage = self.profile["template_usage"]
        
        # 计算最优模板（接受率最高且使用次数 >= 3）
        best_template = None
        best_rate = 0
        
        for template, data in usage.items():
            if data["used"] >= 3:
                rate = data["accepted"] / data["used"]
                if rate > best_rate:
                    best_rate = rate
                    best_template = template
        
        if best_template:
            self.profile["preferences"]["preferred_template"] = best_template
        
        # 动态调整自动接受阈值
        if stats["total_optimizations"] >= 10:
            auto_rate = stats["auto_accepted"] / stats["total_optimizations"]
            # 准确率高，降低阈值（更激进）
            # 准确率低，提高阈值（更保守）
            base_threshold = 0.45
            if auto_rate > 0.8:
                self.profile["preferences"]["auto_accept_threshold"] = base_threshold - 0.1
            elif auto_rate < 0.5:
                self.profile["preferences"]["auto_accept_threshold"] = base_threshold + 0.15
            else:
                self.profile["preferences"]["auto_accept_threshold"] = base_threshold
    
    def get_preferred_template(self) -> Optional[str]:
        """获取用户偏好模板"""
        return self.profile["preferences"].get("preferred_template")
    
    def get_auto_accept_threshold(self) -> float:
        """获取自动接受阈值"""
        threshold = self.profile["preferences"].get("auto_accept_threshold", 0.45)
        
        # 样本少时更保守
        if self.profile["stats"]["total_optimizations"] < 10:
            return max(threshold, 0.5)
        
        return threshold
    
    def get_stats_summary(self) -> Dict:
        """获取统计摘要"""
        stats = self.profile["stats"]
        usage = self.profile["template_usage"]
        
        return {
            "total_queries": stats["total_queries"],
            "total_optimizations": stats["total_optimizations"],
            "auto_accept_rate": (
                stats["auto_accepted"] / stats["total_optimizations"] 
                if stats["total_optimizations"] > 0 else 0
            ),
            "preferred_template": self.get_preferred_template(),
            "template_distribution": {
                t: d["used"] for t, d in usage.items() if d["used"] > 0
            },
            "question_type_distribution": self.profile["question_types"]
        }
    
    def get_recent_queries(self, limit: int = 5) -> List[Dict]:
        """获取最近查询"""
        return self.profile["recent_queries"][-limit:]
    
    def reset_profile(self):
        """重置用户配置"""
        self.profile = self.DEFAULT_PROFILE.copy()
        self.profile["user_id"] = self.user_id
        self.profile["created_at"] = datetime.now().isoformat()
        self.save_profile()


def main():
    """测试入口"""
    import sys
    
    manager = UserProfileManager("test_user")
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "stats":
            print(json.dumps(manager.get_stats_summary(), ensure_ascii=False, indent=2))
        elif cmd == "reset":
            manager.reset_profile()
            print("配置已重置")
        elif cmd == "recent":
            print(json.dumps(manager.get_recent_queries(), ensure_ascii=False, indent=2))
        else:
            print(f"未知命令: {cmd}")
    else:
        # 模拟记录
        manager.record_query(
            query="火箭如何上天？",
            intent="reasoning",
            template="cot",
            action_taken="auto_output",
            user_feedback="accepted"
        )
        print(json.dumps(manager.get_stats_summary(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()