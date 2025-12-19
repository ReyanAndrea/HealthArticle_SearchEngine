"""
Implementasi Vector Space Model dengan TF-IDF
"""

import math
from collections import Counter, defaultdict
import numpy as np

class VectorSpaceModel:
    def __init__(self):
        self.documents = []
        self.vocabulary = set()
        self.inverted_index = defaultdict(list)
        self.idf = {}
        self.doc_vectors = {}
        self.doc_lengths = {}
    
    def build_index(self, processed_documents):
        """Membangun inverted index dan menghitung IDF"""
        self.documents = processed_documents
        
        # Build vocabulary dan inverted index
        for doc in processed_documents:
            doc_id = doc['id']
            tokens = doc['tokens']
            
            # Update vocabulary
            self.vocabulary.update(tokens)
            
            # Build inverted index
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.inverted_index[token].append(doc_id)
        
        # Calculate IDF
        num_docs = len(processed_documents)
        for term in self.vocabulary:
            df = len(self.inverted_index[term])
            self.idf[term] = math.log(num_docs / df) if df > 0 else 0
        
        # Build document vectors
        for doc in processed_documents:
            self.doc_vectors[doc['id']] = self._create_tfidf_vector(doc['tokens'])
            self.doc_lengths[doc['id']] = self._vector_length(self.doc_vectors[doc['id']])
    
    def _create_tfidf_vector(self, tokens):
        """Membuat TF-IDF vector untuk dokumen"""
        tf = Counter(tokens)
        tfidf_vector = {}
        
        for term, freq in tf.items():
            # TF: frekuensi term dalam dokumen
            # IDF: inverse document frequency
            tfidf_vector[term] = freq * self.idf.get(term, 0)
        
        return tfidf_vector
    
    def _vector_length(self, vector):
        """Menghitung panjang vector (untuk normalisasi)"""
        return math.sqrt(sum(val ** 2 for val in vector.values()))
    
    def _cosine_similarity(self, vec1, vec2, vec2_length):
        """Menghitung cosine similarity antara dua vector"""
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in vec1)
        
        vec1_length = self._vector_length(vec1)
        
        if vec1_length == 0 or vec2_length == 0:
            return 0
        
        return dot_product / (vec1_length * vec2_length)
    
    def search(self, query_tokens, top_k=10):
        """Mencari dokumen yang relevan dengan query"""
        if not query_tokens:
            return []
        
        # Create query vector
        query_vector = self._create_tfidf_vector(query_tokens)
        
        # Optimize: Get candidate documents yang mengandung minimal satu query term
        candidate_doc_ids = set()
        for term in query_tokens:
            if term in self.inverted_index:
                candidate_doc_ids.update(self.inverted_index[term])
        
        # If no candidates, search all documents
        if not candidate_doc_ids:
            candidate_doc_ids = set(d['id'] for d in self.documents)
        
        # Calculate similarity hanya untuk candidate documents
        scores = []
        for doc in self.documents:
            doc_id = doc['id']
            if doc_id not in candidate_doc_ids:
                continue
            
            similarity = self._cosine_similarity(
                query_vector,
                self.doc_vectors[doc_id],
                self.doc_lengths[doc_id]
            )
            
            if similarity > 0:
                scores.append({
                    'doc_id': doc_id,
                    'title': doc['title'],
                    'content': doc['content'],
                    'url': doc['url'],
                    'date': doc['date'],
                    'score': similarity
                })
        
        # Sort by score (descending)
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return scores[:top_k]
    
    def get_stats(self):
        """Mendapatkan statistik index"""
        return {
            'num_documents': len(self.documents),
            'vocabulary_size': len(self.vocabulary),
            'avg_doc_length': np.mean([len(doc['tokens']) for doc in self.documents])
        }