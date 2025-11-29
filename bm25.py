"""
Implementasi Algoritma BM25
"""

import math
from collections import Counter, defaultdict
import numpy as np

class BM25:
    def __init__(self, k1=1.5, b=0.75):
        """
        k1: parameter yang mengontrol saturasi term frequency (default: 1.5)
        b: parameter yang mengontrol normalisasi panjang dokumen (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        self.documents = []
        self.inverted_index = defaultdict(list)
        self.doc_freqs = {}
        self.idf = {}
        self.doc_len = {}
        self.avgdl = 0
    
    def build_index(self, processed_documents):
        """Membangun index untuk BM25"""
        self.documents = processed_documents
        
        # Calculate document lengths
        total_len = 0
        for doc in processed_documents:
            doc_id = doc['id']
            doc_tokens = doc['tokens']
            self.doc_len[doc_id] = len(doc_tokens)
            total_len += len(doc_tokens)
            
            # Count term frequencies in document
            self.doc_freqs[doc_id] = Counter(doc_tokens)
            
            # Build inverted index
            unique_tokens = set(doc_tokens)
            for token in unique_tokens:
                self.inverted_index[token].append(doc_id)
        
        # Calculate average document length
        self.avgdl = total_len / len(processed_documents) if processed_documents else 0
        
        # Calculate IDF for each term
        num_docs = len(processed_documents)
        for term, doc_list in self.inverted_index.items():
            df = len(doc_list)
            # BM25 IDF formula - use more standard version
            # idf = log((N - df + 0.5) / (df + 0.5)) with constant +1 for numerical stability
            self.idf[term] = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)
    
    def _score_document(self, query_tokens, doc_id):
        """Menghitung BM25 score untuk satu dokumen"""
        score = 0.0
        doc_len = self.doc_len[doc_id]
        
        for term in query_tokens:
            if term not in self.doc_freqs[doc_id]:
                continue
            
            # Term frequency in document
            tf = self.doc_freqs[doc_id][term]
            
            # IDF
            idf = self.idf.get(term, 0)
            
            # BM25 formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
            
            score += idf * (numerator / denominator)
        
        return score
    
    def search(self, query_tokens, top_k=10):
        """Mencari dokumen yang relevan dengan query menggunakan BM25"""
        if not query_tokens:
            return []
        
        # Get candidate documents (documents yang mengandung setidaknya satu query term)
        candidate_docs = set()
        for term in query_tokens:
            if term in self.inverted_index:
                candidate_docs.update(self.inverted_index[term])
        
        # Jika tidak ada candidate, cari di semua dokumen
        if not candidate_docs:
            candidate_docs = set(d['id'] for d in self.documents)
        
        # Calculate BM25 score untuk setiap candidate document
        scores = []
        for doc_id in candidate_docs:
            doc = next((d for d in self.documents if d['id'] == doc_id), None)
            if doc:
                score = self._score_document(query_tokens, doc_id)
                scores.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'content': doc['content'],
                    'url': doc['url'],
                    'date': doc['date'],
                    'score': score
                })
        
        # Sort by score (descending)
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return scores[:top_k]
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return scores[:top_k]
    
    def get_stats(self):
        """Mendapatkan statistik index"""
        return {
            'num_documents': len(self.documents),
            'vocabulary_size': len(self.inverted_index),
            'avg_doc_length': self.avgdl,
            'k1': self.k1,
            'b': self.b
        }