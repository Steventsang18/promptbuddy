#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Model Semantic Engine for Prompt Engineering
支持多种语义模型的集成框架
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from abc import ABC, abstractmethod

class SemanticModel(ABC):
    """语义模型基类"""
    
    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        """分析文本并返回语义特征"""
        pass
    
    @abstractmethod
    def get_intent_score(self, text: str, intent_type: str) -> float:
        """计算特定意图的匹配分数"""
        pass

class KeywordBasedModel(SemanticModel):
    """基于关键词的语义模型（现有模型）"""
    
    def __init__(self):
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
        
        self.simple_query_patterns = [
            r'今天.*天气.*', r'明天.*天气.*', r'.*天气怎么样.*',
            r'你好.*', r'在吗.*', r'谢谢.*', r'好的.*'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """文本预处理"""
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
            for keyword in self.intent_keywords['reasoning']['science_tech']:
                if keyword in text:
                    score += 0.3
            for keyword in self.intent_keywords['reasoning']['math_logic']:
                if keyword in text:
                    score += 0.25
            for pattern in self.intent_keywords['reasoning']['question_patterns']:
                if re.search(pattern, text):
                    score += 0.2
            if len(text) > 15:
                score += 0.1
                
        elif intent_type == 'decomposition':
            for verb in self.intent_keywords['decomposition']['action_verbs']:
                if verb in text:
                    score += 0.3
            for word in self.intent_keywords['decomposition']['project_words']:
                if word in text:
                    score += 0.25
            for pattern in self.intent_keywords['decomposition']['question_patterns']:
                if re.search(pattern, text):
                    score += 0.3
            if len(text) > 20:
                score += 0.15
                
        elif intent_type == 'criticism':
            for word in self.intent_keywords['criticism']['quality_words']:
                if word in text:
                    score += 0.4
            for pattern in self.intent_keywords['criticism']['question_patterns']:
                if re.search(pattern, text):
                    score += 0.3
        
        return min(score, 1.0)
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """分析文本语义特征"""
        text = self.preprocess_text(text)
        features = {
            'is_simple_query': self.is_simple_query(text),
            'word_count': len(text.split()),
            'char_count': len(text),
            'has_question_mark': '?' in text or '？' in text,
            'semantic_scores': {}
        }
        
        for intent_type in ['reasoning', 'decomposition', 'criticism']:
            features['semantic_scores'][intent_type] = self.calculate_semantic_score(text, intent_type)
        
        return features
    
    def get_intent_score(self, text: str, intent_type: str) -> float:
        """获取意图分数"""
        features = self.analyze(text)
        if features['is_simple_query'] and intent_type != 'simple':
            return 0.0
        return features['semantic_scores'].get(intent_type, 0.0)

class PatternBasedModel(SemanticModel):
    """基于模式的语义模型"""
    
    def __init__(self):
        # 复杂句式模式
        self.patterns = {
            'reasoning': [
                r'(?:怎么|如何|为什么).*?(?:实现|工作|运作|运行)',
                r'(?:解释|说明|描述).*?(?:原理|机制|过程)',
                r'(?:分析|研究|探讨).*?(?:原因|因素|影响)',
                r'(?:计算|求解|推导).*?(?:结果|答案|值)'
            ],
            'decomposition': [
                r'(?:如何|怎样).*?(?:从零开始|逐步|一步步).*?(?:建立|创建|开发)',
                r'(?:制定|设计|规划).*?(?:完整|详细|全面).*?(?:方案|计划|策略)',
                r'(?:步骤|流程|方法).*?(?:实现|完成|达成)',
                r'(?:分阶段|分步骤).*?(?:实施|执行|推进)'
            ],
            'criticism': [
                r'(?:检查|验证|审核).*?(?:质量|正确性|准确性)',
                r'(?:评估|评价|评判).*?(?:效果|性能|效率)',
                r'(?:改进|优化|提升).*?(?:方案|方法|策略)',
                r'(?:潜在|可能).*?(?:问题|风险|缺陷)'
            ]
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """分析文本模式特征"""
        features = {
            'pattern_matches': {},
            'complexity_indicators': {
                'has_complex_structure': len(text.split()) > 8,
                'has_multiple_clauses': text.count('，') + text.count(',') > 1,
                'has_technical_language': any(term in text for term in 
                    ['算法', '模型', '系统', '架构', '框架', '协议', '机制'])
            }
        }
        
        for intent_type, patterns in self.patterns.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    matches += 1
            features['pattern_matches'][intent_type] = matches
        
        return features
    
    def get_intent_score(self, text: str, intent_type: str) -> float:
        """获取基于模式的意图分数"""
        features = self.analyze(text)
        pattern_score = features['pattern_matches'].get(intent_type, 0) * 0.25
        
        # 复杂度加分
        complexity_bonus = 0.0
        if features['complexity_indicators']['has_complex_structure']:
            complexity_bonus += 0.1
        if features['complexity_indicators']['has_multiple_clauses']:
            complexity_bonus += 0.05
        if features['complexity_indicators']['has_technical_language']:
            complexity_bonus += 0.15
        
        total_score = min(pattern_score + complexity_bonus, 1.0)
        return total_score

class ContextAwareModel(SemanticModel):
    """上下文感知语义模型"""
    
    def __init__(self):
        # 上下文关键词和领域识别
        self.domain_keywords = {
            'technical': ['AI', '机器学习', '深度学习', '神经网络', '算法', '代码', '编程'],
            'business': ['营销', '销售', '市场', '客户', '收入', '利润', '战略'],
            'creative': ['写作', '设计', '创意', '艺术', '文案', '内容'],
            'academic': ['研究', '论文', '学术', '理论', '实验', '数据']
        }
        
        # 意图-领域映射
        self.intent_domain_mapping = {
            'reasoning': ['technical', 'academic'],
            'decomposition': ['business', 'technical'],
            'criticism': ['technical', 'business', 'academic']
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """分析上下文特征"""
        features = {
            'detected_domains': [],
            'domain_confidence': {},
            'context_indicators': {
                'has_domain_specific_terms': False,
                'has_professional_language': any(term in text for term in 
                    ['专业', '专家', '最佳实践', '标准', '规范']),
                'has_action_oriented_language': any(term in text for term in 
                    ['执行', '实施', '完成', '达成', '实现'])
            }
        }
        
        # 领域检测
        for domain, keywords in self.domain_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > 0:
                features['detected_domains'].append(domain)
                features['domain_confidence'][domain] = min(matches * 0.2, 1.0)
        
        features['context_indicators']['has_domain_specific_terms'] = len(features['detected_domains']) > 0
        
        return features
    
    def get_intent_score(self, text: str, intent_type: str) -> float:
        """获取基于上下文的意图分数"""
        features = self.analyze(text)
        
        # 基于领域的分数
        domain_score = 0.0
        relevant_domains = self.intent_domain_mapping.get(intent_type, [])
        for domain in relevant_domains:
            if domain in features['domain_confidence']:
                domain_score = max(domain_score, features['domain_confidence'][domain])
        
        # 上下文指标加分
        context_bonus = 0.0
        if features['context_indicators']['has_domain_specific_terms']:
            context_bonus += 0.1
        if features['context_indicators']['has_professional_language']:
            context_bonus += 0.15
        if features['context_indicators']['has_action_oriented_language'] and intent_type == 'decomposition':
            context_bonus += 0.2
        
        total_score = min(domain_score + context_bonus, 1.0)
        return total_score

class MultiModelEngine:
    """多模型语义引擎"""
    
    def __init__(self):
        self.models = {
            'keyword': KeywordBasedModel(),
            'pattern': PatternBasedModel(),
            'context': ContextAwareModel()
        }
        
        # 模型权重配置
        self.model_weights = {
            'keyword': 0.4,
            'pattern': 0.35,
            'context': 0.25
        }
    
    def ensemble_analyze(self, text: str) -> Dict[str, Any]:
        """集成分析"""
        results = {}
        model_scores = {}
        
        # 获取各模型的分析结果
        for model_name, model in self.models.items():
            try:
                model_scores[model_name] = {}
                for intent_type in ['reasoning', 'decomposition', 'criticism']:
                    score = model.get_intent_score(text, intent_type)
                    model_scores[model_name][intent_type] = score
            except Exception as e:
                print(f"Model {model_name} failed: {e}")
                model_scores[model_name] = {'reasoning': 0.0, 'decomposition': 0.0, 'criticism': 0.0}
        
        # 集成分数计算（加权平均）
        ensemble_scores = {}
        for intent_type in ['reasoning', 'decomposition', 'criticism']:
            weighted_score = 0.0
            for model_name, weight in self.model_weights.items():
                weighted_score += model_scores[model_name][intent_type] * weight
            ensemble_scores[intent_type] = weighted_score
        
        # 简单查询检测（优先级最高）
        is_simple = self.models['keyword'].is_simple_query(text)
        if is_simple:
            for intent_type in ensemble_scores:
                ensemble_scores[intent_type] = 0.0
        
        results = {
            'original_input': text,
            'ensemble_scores': ensemble_scores,
            'model_scores': model_scores,
            'is_simple_query': is_simple,
            'best_intent': max(ensemble_scores, key=ensemble_scores.get) if not is_simple else 'simple',
            'confidence': max(ensemble_scores.values()) if not is_simple else 0.9
        }
        
        return results

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 multi_model_engine.py \"input text\"")
        sys.exit(1)
    
    input_text = sys.argv[1]
    engine = MultiModelEngine()
    
    result = engine.ensemble_analyze(input_text)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()