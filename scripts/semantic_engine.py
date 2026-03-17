#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Semantic Engine for Prompt Engineering
基于本地方法的语义理解引擎（无需下载模型）
"""

import os
import re
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import Counter
from datetime import datetime


class LocalSemanticEngine:
    """本地语义引擎 - 使用 TF-IDF 和词向量"""
    
    # 意图参考句子
    INTENT_EXAMPLES = {
        "reasoning": [
            "火箭如何上天",
            "为什么天是蓝的",
            "解释一下量子力学原理",
            "黑洞是怎么形成的",
            "光速为什么是最快的",
            "地球为什么有引力",
            "分析这个问题的原因",
            "为什么会出现这个现象",
            "这个技术的原理是什么",
            "推导一下这个公式",
            "证明这个定理",
            "解这个方程",
            "计算一下概率",
            "数学证明",
        ],
        "decomposition": [
            "如何创建一个项目",
            "从零开始建立一个系统",
            "制定一个完整的计划",
            "建立一套工作流程",
            "如何搭建一个平台",
            "构建一个完整的体系",
            "设计一个解决方案",
            "规划项目实施步骤",
            "制定运营策略",
            "如何开展一个项目",
            "项目实施的步骤",
            "怎么做这件事",
            "有什么方法可以",
            "给我一个行动指南",
        ],
        "criticism": [
            "检查这篇文章的问题",
            "审核一下这个方案",
            "评估这个设计",
            "找出潜在风险",
            "验证这个结论",
            "改进这个方案",
            "优化这个流程",
            "这个有什么问题",
            "检查有没有错误",
            "审查一下质量",
            "评估一下效果",
            "分析存在哪些问题",
            "诊断一下原因",
        ],
        "simple": [
            "你好",
            "在吗",
            "谢谢",
            "好的",
            "今天天气",
            "明天天气",
            "几点了",
            "现在时间",
        ]
    }
    
    def __init__(self):
        """初始化本地语义引擎"""
        self.vocabulary = set()
        self.idf_scores = {}
        self.intent_vectors = {}
        
        self._build_vocabulary()
        self._compute_idf()
        self._precompute_intent_vectors()
    
    def _tokenize(self, text: str) -> List[str]:
        """简单分词"""
        # 移除标点
        text = re.sub(r'[，。！？、；：""''（）【】\\s]+', ' ', text)
        # 分词（简单的字符级 + 词语级混合）
        words = text.strip().split()
        # 添加字符级特征
        chars = list(text)
        return words + chars
    
    def _build_vocabulary(self):
        """构建词汇表"""
        for examples in self.INTENT_EXAMPLES.values():
            for example in examples:
                tokens = self._tokenize(example)
                self.vocabulary.update(tokens)
    
    def _compute_idf(self):
        """计算 IDF 分数"""
        doc_count = 0
        doc_freq = Counter()
        
        # 统计文档频率
        for examples in self.INTENT_EXAMPLES.values():
            for example in examples:
                tokens = set(self._tokenize(example))
                for token in tokens:
                    doc_freq[token] += 1
                doc_count += 1
        
        # 计算 IDF
        for token, freq in doc_freq.items():
            self.idf_scores[token] = np.log((doc_count + 1) / (freq + 1)) + 1
    
    def _compute_tfidf(self, text: str) -> np.ndarray:
        """计算文本的 TF-IDF 向量"""
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        
        # 创建向量
        vector = np.zeros(len(self.vocabulary))
        vocab_list = list(self.vocabulary)
        
        for i, word in enumerate(vocab_list):
            if word in tf:
                tf_score = tf[word] / len(tokens)
                idf_score = self.idf_scores.get(word, 1.0)
                vector[i] = tf_score * idf_score
        
        # L2 归一化
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def _precompute_intent_vectors(self):
        """预计算意图向量"""
        for intent, examples in self.INTENT_EXAMPLES.items():
            vectors = [self._compute_tfidf(ex) for ex in examples]
            # 取平均向量
            self.intent_vectors[intent] = np.mean(vectors, axis=0)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(vec1, vec2) / (norm1 * norm2)
    
    def classify(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        分类用户输入
        
        Returns:
            (best_intent, confidence, all_scores)
        """
        # 计算输入向量
        text_vector = self._compute_tfidf(text)
        
        # 计算与各意图的相似度
        scores = {}
        for intent, intent_vector in self.intent_vectors.items():
            similarity = self._cosine_similarity(text_vector, intent_vector)
            scores[intent] = similarity
        
        # 找到最佳意图
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        # 将相似度转换为更直观的置信度
        confidence = max(0, min(1, confidence * 2))  # 放大并限制在 0-1
        
        return best_intent, confidence, scores
    
    def get_intent_examples(self, intent: str) -> List[str]:
        """获取某意图的例子"""
        return self.INTENT_EXAMPLES.get(intent, [])


class SemanticEngine:
    """语义引擎 - 支持多种后端"""
    
    def __init__(self, backend: str = "local"):
        """
        初始化语义引擎
        
        Args:
            backend: 后端类型 "local" | "transformers"
        """
        self.backend = backend
        self.is_available = True
        
        if backend == "local":
            self.engine = LocalSemanticEngine()
        else:
            # 尝试加载 transformers 后端
            try:
                from sentence_transformers import SentenceTransformer
                self.engine = self._load_transformers_backend()
            except ImportError:
                print("Warning: transformers not available, using local backend")
                self.engine = LocalSemanticEngine()
                self.backend = "local"
    
    def _load_transformers_backend(self):
        """加载 transformers 后端（如果可用）"""
        # 这里可以加载真正的 transformer 模型
        # 目前回退到本地引擎
        return LocalSemanticEngine()
    
    def classify(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """分类用户输入"""
        return self.engine.classify(text)


class HybridIntentDetector:
    """混合意图检测器 - 结合关键词和语义两种方法"""
    
    def __init__(self, semantic_engine: SemanticEngine = None):
        """初始化混合检测器"""
        self.semantic_engine = semantic_engine or SemanticEngine()
    
    def detect(self, text: str, 
               keyword_result: Dict = None,
               use_fusion: bool = True) -> Dict:
        """
        混合检测意图
        
        Args:
            text: 用户输入
            keyword_result: 关键词检测结果（可选）
            use_fusion: 是否使用融合策略
        
        Returns:
            {
                "intent": str,
                "confidence": float,
                "method": str,
                "scores": dict
            }
        """
        # 语义检测
        sem_intent, sem_conf, sem_scores = self.semantic_engine.classify(text)
        
        if keyword_result is None or not use_fusion:
            return {
                "intent": sem_intent,
                "confidence": sem_conf,
                "method": "semantic",
                "scores": sem_scores
            }
        
        # 获取关键词结果
        kw_intent = keyword_result.get("intent", "simple")
        kw_conf = keyword_result.get("confidence", 0)
        
        # 融合策略
        return self._fuse_results(
            text=text,
            sem_intent=sem_intent,
            sem_conf=sem_conf,
            sem_scores=sem_scores,
            kw_intent=kw_intent,
            kw_conf=kw_conf
        )
    
    def _fuse_results(self,
                     text: str,
                     sem_intent: str,
                     sem_conf: float,
                     sem_scores: Dict,
                     kw_intent: str,
                     kw_conf: float) -> Dict:
        """融合语义和关键词结果"""
        # 关键词高置信度，直接使用
        if kw_conf > 0.7:
            return {
                "intent": kw_intent,
                "confidence": kw_conf,
                "method": "keyword_high_conf",
                "scores": sem_scores
            }
        
        # 语义高置信度，使用语义
        if sem_conf > 0.6:
            return {
                "intent": sem_intent,
                "confidence": sem_conf,
                "method": "semantic_high_conf",
                "scores": sem_scores
            }
        
        # 两者一致，增强置信度
        if sem_intent == kw_intent:
            fused_conf = max(sem_conf, kw_conf) * 1.15
            fused_conf = min(fused_conf, 0.95)
            return {
                "intent": sem_intent,
                "confidence": fused_conf,
                "method": "fusion_agree",
                "scores": sem_scores
            }
        
        # 不一致，根据文本长度选择
        # 长文本更信任语义，短文本更信任关键词
        if len(text) > 15:
            return {
                "intent": sem_intent,
                "confidence": sem_conf,
                "method": "semantic_wins_long",
                "scores": sem_scores
            }
        else:
            # 短文本，关键词可能更准确
            if kw_conf > sem_conf:
                return {
                    "intent": kw_intent,
                    "confidence": kw_conf,
                    "method": "keyword_wins_short",
                    "scores": sem_scores
                }
            else:
                return {
                    "intent": sem_intent,
                    "confidence": sem_conf,
                    "method": "semantic_wins",
                    "scores": sem_scores
                }


def main():
    """测试入口"""
    print("=" * 50)
    print("Local Semantic Engine Test")
    print("=" * 50)
    
    engine = LocalSemanticEngine()
    
    test_cases = [
        "火箭如何上天？",
        "如何建立一个完整的运营体系？",
        "检查这篇文章有没有问题",
        "你好，在吗？",
        "为什么光速是最快的？",
        "制定一个营销计划",
        "今天天气怎么样",
        "分析一下这个数据的问题",
    ]
    
    print("\n📊 测试结果:")
    print("-" * 50)
    
    for text in test_cases:
        intent, conf, scores = engine.classify(text)
        print(f"\n输入: {text}")
        print(f"  → 意图: {intent}")
        print(f"  → 置信度: {conf:.2f}")
        print(f"  → 各项得分: ", end="")
        for i, s in sorted(scores.items(), key=lambda x: -x[1]):
            print(f"{i}:{s:.2f} ", end="")
        print()


if __name__ == "__main__":
    main()