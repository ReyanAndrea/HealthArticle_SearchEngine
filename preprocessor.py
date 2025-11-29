"""
Text Preprocessing untuk Bahasa Indonesia
"""

import re
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class IndonesianPreprocessor:
    def __init__(self):
        # Download NLTK data jika belum ada
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
            except:
                pass
        
        # Inisialisasi Sastrawi
        self.stemmer = StemmerFactory().create_stemmer()
        self.stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
        
        # Stopwords tambahan untuk domain kesehatan
        self.additional_stopwords = set([
            'dan', 'atau', 'yang', 'ini', 'itu', 'pada', 'dengan', 'untuk',
            'dari', 'ke', 'di', 'oleh', 'adalah', 'akan', 'dapat', 'telah',
            'ada', 'juga', 'seperti', 'lebih', 'bisa', 'sudah', 'hanya'
        ])
    
    def clean_text(self, text):
        """Membersihkan teks dari karakter khusus"""
        if not text:
            return ""
        
        # Lowercase
        text = text.lower()
        
        # Hapus URL
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Hapus email
        text = re.sub(r'\S+@\S+', '', text)
        
        # Hapus angka
        text = re.sub(r'\d+', '', text)
        
        # Hapus karakter khusus, tapi pertahankan spasi
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Hapus spasi berlebih
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text):
        """Tokenisasi teks"""
        # Gunakan split sederhana untuk bahasa Indonesia
        tokens = text.split()
        return tokens
    
    def remove_stopwords(self, tokens):
        """Menghapus stopwords"""
        # Filter stopwords
        filtered_tokens = [
            token for token in tokens 
            if token not in self.additional_stopwords and len(token) > 2
        ]
        return filtered_tokens
    
    def stem(self, tokens):
        """Stemming menggunakan Sastrawi"""
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens
    
    def preprocess(self, text):
        """Pipeline preprocessing lengkap"""
        # 1. Clean text
        text = self.clean_text(text)
        
        # 2. Tokenize
        tokens = self.tokenize(text)
        
        # 3. Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # 4. Stemming
        tokens = self.stem(tokens)
        
        return tokens
    
    def preprocess_documents(self, documents):
        """Preprocess multiple documents"""
        processed_docs = []
        
        for doc in documents:
            # Gabungkan title dan content
            full_text = f"{doc.get('title', '')} {doc.get('content', '')}"
            tokens = self.preprocess(full_text)
            
            processed_docs.append({
                'id': doc.get('id'),
                'title': doc.get('title'),
                'content': doc.get('content'),
                'tokens': tokens,
                'url': doc.get('url'),
                'date': doc.get('date')
            })
        
        return processed_docs