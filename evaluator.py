"""
Modul Evaluasi untuk mengukur performa sistem IR
"""

import numpy as np

class IREvaluator:
    def __init__(self):
        self.test_queries = []
        self.relevance_judgments = {}
    
    def add_test_query(self, query_id, query_text, relevant_doc_ids):
        """Menambahkan test query dengan ground truth"""
        self.test_queries.append({
            'id': query_id,
            'text': query_text
        })
        self.relevance_judgments[query_id] = set(relevant_doc_ids)
    
    def precision(self, retrieved_docs, relevant_docs):
        """
        Precision = |retrieved ∩ relevant| / |retrieved|
        """
        if not retrieved_docs:
            return 0.0
        
        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)
        
        intersection = retrieved_set.intersection(relevant_set)
        
        return len(intersection) / len(retrieved_set)
    
    def recall(self, retrieved_docs, relevant_docs):
        """
        Recall = |retrieved ∩ relevant| / |relevant|
        """
        if not relevant_docs:
            return 0.0
        
        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)
        
        intersection = retrieved_set.intersection(relevant_set)
        
        return len(intersection) / len(relevant_set)
    
    def f1_score(self, precision, recall):
        """
        F1-Score = 2 * (precision * recall) / (precision + recall)
        """
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def average_precision(self, retrieved_docs, relevant_docs):
        """
        Average Precision untuk satu query
        """
        if not relevant_docs:
            return 0.0
        
        relevant_set = set(relevant_docs)
        precision_sum = 0.0
        num_relevant_found = 0
        
        for i, doc_id in enumerate(retrieved_docs, 1):
            if doc_id in relevant_set:
                num_relevant_found += 1
                precision_at_i = num_relevant_found / i
                precision_sum += precision_at_i
        
        if num_relevant_found == 0:
            return 0.0
        
        return precision_sum / len(relevant_set)
    
    def mean_average_precision(self, all_retrieved_docs, all_relevant_docs):
        """
        MAP = rata-rata dari AP untuk semua query
        """
        if not all_retrieved_docs:
            return 0.0
        
        ap_sum = 0.0
        for query_id, retrieved_docs in all_retrieved_docs.items():
            relevant_docs = all_relevant_docs.get(query_id, [])
            ap = self.average_precision(retrieved_docs, relevant_docs)
            ap_sum += ap
        
        return ap_sum / len(all_retrieved_docs)
    
    def evaluate_query(self, retrieved_doc_ids, relevant_doc_ids, k=10):
        """Evaluasi untuk satu query"""
        # Ambil top-k retrieved documents
        retrieved_top_k = retrieved_doc_ids[:k]
        
        # Calculate metrics
        prec = self.precision(retrieved_top_k, relevant_doc_ids)
        rec = self.recall(retrieved_top_k, relevant_doc_ids)
        f1 = self.f1_score(prec, rec)
        ap = self.average_precision(retrieved_top_k, relevant_doc_ids)
        
        return {
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'average_precision': ap
        }
    
    def evaluate_system(self, search_results_by_query, k=10):
        """Evaluasi keseluruhan sistem dengan multiple queries"""
        all_metrics = []
        all_retrieved = {}
        all_relevant = {}
        
        for query_id, results in search_results_by_query.items():
            retrieved_doc_ids = [r['doc_id'] for r in results]
            relevant_doc_ids = self.relevance_judgments.get(query_id, [])
            
            all_retrieved[query_id] = retrieved_doc_ids[:k]
            all_relevant[query_id] = relevant_doc_ids
            
            metrics = self.evaluate_query(retrieved_doc_ids, relevant_doc_ids, k)
            all_metrics.append(metrics)
        
        # Calculate average metrics
        avg_metrics = {
            'precision': np.mean([m['precision'] for m in all_metrics]),
            'recall': np.mean([m['recall'] for m in all_metrics]),
            'f1_score': np.mean([m['f1_score'] for m in all_metrics]),
            'MAP': self.mean_average_precision(all_retrieved, all_relevant)
        }
        
        return avg_metrics, all_metrics