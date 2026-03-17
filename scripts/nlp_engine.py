#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Advanced NLP Engine for Prompt Engineering
基于语义理解的意图识别系统
"""

import re
import json
from typing import Dict, List, Tuple, Optional

class NLPEngine:
    def __init__(self):
        # 语义关键词库（按意图分类）
        self.intent_keywords = {
            'reasoning': {
                'science_tech': [
                    '火箭', '物理', '化学', '生物', '工程', '技术', '科学', 
                    '工作原理', '机制', '定律', '公式', '理论', '现象', '过程',
                    '天空', '地球', '宇宙', '星星', '太阳', '月亮', '海洋', 
                    '大气', '光', '声音', '电', '磁', '量子', '相对论'
                ],
                'math_logic': [
                    '数学', '计算', '推理', '分析', '证明', '解', '方程', 
                    '几何', '统计', '概率', '逻辑', '算法', '优化'
                ],
                'question_patterns': [
                    r'怎么.*', r'如何.*', r'为什么.*', r'.*原理.*', 
                    r'.*机制.*', r'.*工作原理.*'
                ]
            },
            'decomposition': {
                'action_verbs': [
                    '建立', '创建', '开发', '构建', '制定', '设计', '规划',
                    '实施', '执行', '启动', '开展', '推进', '完成'
                ],
                'project_words': [
                    '步骤', '流程', '计划', '方案', '策略', '方法', '指南',
                    '项目', '产品', '公司', '团队', '系统', '平台'
                ],
                'question_patterns': [
                    r'如何.*建立.*', r'如何.*创建.*', r'如何.*开发.*',
                    r'如何.*制定.*', r'如何.*设计.*', r'如何.*规划.*'
                ]
            },
            'criticism': {
                'quality_words': [
                    '检查', '验证', '质量', '审核', '评估', '审查', '改进',
                    '优化', '测试', 'bug', '错误', '问题', '风险', '缺陷'
                ],
                'question_patterns': [
                    r'.*检查.*', r'.*验证.*', r'.*质量.*', r'.*审核.*',
                    r'.*评估.*', r'.*审查.*', r'.*改进.*', r'.*优化.*'
                ]
            }
        }
        
        # 简单查询排除词
        self.simple_query_patterns = [
            r'今天.*天气.*', r'明天.*天气.*', r'.*天气怎么样.*',
            r'你好.*', r'在吗.*', r'谢谢.*', r'好的.*'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """文本预处理"""
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def is_simple_query(self, text: str) -> bool:
        """判断是否为简单查询"""
        for pattern in self.simple_query_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def calculate_semantic_score(self, text: str, intent_type: str) -> float:
        """计算语义匹配分数"""
        score = 0.0
        
        if intent_type == 'reasoning':
            # 检查科学/技术关键词
            for keyword in self.intent_keywords['reasoning']['science_tech']:
                if keyword in text:
                    score += 0.3
            
            # 检查数学/逻辑关键词  
            for keyword in self.intent_keywords['reasoning']['math_logic']:
                if keyword in text:
                    score += 0.25
            
            # 检查疑问句模式
            for pattern in self.intent_keywords['reasoning']['question_patterns']:
                if re.search(pattern, text):
                    score += 0.2
            
            # 长度加分（复杂问题通常较长）
            if len(text) > 15:
                score += 0.1
                
        elif intent_type == 'decomposition':
            # 检查动作动词
            for verb in self.intent_keywords['decomposition']['action_verbs']:
                if verb in text:
                    score += 0.3
            
            # 检查项目相关词汇
            for word in self.intent_keywords['decomposition']['project_words']:
                if word in text:
                    score += 0.25
            
            # 检查复合疑问句模式
            for pattern in self.intent_keywords['decomposition']['question_patterns']:
                if re.search(pattern, text):
                    score += 0.3
            
            # 长度加分
            if len(text) > 20:
                score += 0.15
                
        elif intent_type == 'criticism':
            # 检查质量相关词汇
            for word in self.intent_keywords['criticism']['quality_words']:
                if word in text:
                    score += 0.4
            
            # 检查质量相关模式
            for pattern in self.intent_keywords['criticism']['question_patterns']:
                if re.search(pattern, text):
                    score += 0.3
        
        return min(score, 1.0)  # 限制最大分数为1.0
    
    def detect_intent_with_nlp(self, text: str) -> Tuple[str, float]:
        """使用NLP进行意图识别"""
        text = self.preprocess_text(text)
        
        # 简单查询直接返回
        if self.is_simple_query(text):
            return 'simple', 0.9
        
        # 计算各意图的语义分数
        scores = {}
        for intent_type in ['reasoning', 'decomposition', 'criticism']:
            scores[intent_type] = self.calculate_semantic_score(text, intent_type)
        
        # 找到最高分的意图
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]
        
        # 如果最高分低于阈值，返回简单意图
        if best_score < 0.3:
            return 'simple', 0.8
        
        return best_intent, best_score
    
    def analyze_complexity(self, text: str) -> Dict[str, any]:
        """分析文本复杂度"""
        analysis = {
            'word_count': len(text.split()),
            'char_count': len(text),
            'has_question_mark': '?' in text or '？' in text,
            'has_complex_verbs': any(verb in text for verb in 
                ['分析', '解决', '理解', '解释', '证明', '计算']),
            'has_technical_terms': any(term in text for term in 
                ['算法', '模型', '系统', '架构', '框架', '协议'])
        }
        return analysis

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 nlp_engine.py \"input text\"")
        sys.exit(1)
    
    input_text = sys.argv[1]
    engine = NLPEngine()
    
    intent, confidence = engine.detect_intent_with_nlp(input_text)
    complexity = engine.analyze_complexity(input_text)
    
    result = {
        'original_input': input_text,
        'detected_intent': intent,
        'confidence_score': round(confidence, 2),
        'complexity_analysis': complexity
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()