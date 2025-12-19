"""
Data Loader - Load artikel dari file JSON hasil scraping
"""

import json
import os

class DataLoader:
    def __init__(self, json_file='articles_data.json'):
        self.json_file = json_file
        self.articles = []
    
    def load_from_json(self):
        """Load artikel dari file JSON"""
        if not os.path.exists(self.json_file):
            print(f"File {self.json_file} tidak ditemukan!")
            print("Jalankan scraper.py terlebih dahulu untuk mengumpulkan data.")
            return []
        
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.articles = json.load(f)
            print(f"Berhasil load {len(self.articles)} artikel dari {self.json_file}")
            return self.articles
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return []
    
    def get_statistics(self):
        """Dapatkan statistik dari dataset"""
        if not self.articles:
            return None
        
        # Hitung statistik
        total_articles = len(self.articles)
        
        # Sumber artikel
        sources = {}
        for article in self.articles:
            source = article.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        # Panjang konten
        content_lengths = [len(article.get('content', '')) for article in self.articles]
        avg_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
        
        return {
            'total_articles': total_articles,
            'sources': sources,
            'avg_content_length': avg_length,
            'min_content_length': min(content_lengths) if content_lengths else 0,
            'max_content_length': max(content_lengths) if content_lengths else 0
        }
    
    def print_statistics(self):
        """Print statistik dataset"""
        stats = self.get_statistics()
        
        if not stats:
            print("Tidak ada data untuk ditampilkan")
            return
        
        print("\n" + "="*60)
        print("STATISTIK DATASET")
        print("="*60)
        print(f"Total Artikel: {stats['total_articles']}")
        print(f"Rata-rata Panjang Konten: {stats['avg_content_length']:.0f} karakter")
        print(f"Panjang Min: {stats['min_content_length']} karakter")
        print(f"Panjang Max: {stats['max_content_length']} karakter")
        
        print("\nDistribusi per Sumber:")
        for source, count in stats['sources'].items():
            percentage = (count / stats['total_articles']) * 100
            print(f"  - {source}: {count} artikel ({percentage:.1f}%)")
        print("="*60)
    
    def sample_articles(self, n=5):
        """Tampilkan sample artikel"""
        if not self.articles:
            print("Tidak ada artikel untuk ditampilkan")
            return
        
        print(f"\nSAMPLE {min(n, len(self.articles))} ARTIKEL:")
        print("="*60)
        
        for i, article in enumerate(self.articles[:n], 1):
            print(f"\n{i}. {article.get('title', 'No Title')}")
            print(f"   Sumber: {article.get('source', 'Unknown')}")
            print(f"   URL: {article.get('url', '')}")
            content = article.get('content', '')
            print(f"   Konten: {content[:150]}...")
            print("-"*60)

def main():
    """Main function untuk testing"""
    loader = DataLoader('articles_data.json')
    
    # Load data
    articles = loader.load_from_json()
    
    if articles:
        # Print statistik
        loader.print_statistics()
        
        # Sample artikel
        loader.sample_articles(n=5)

if __name__ == "__main__":
    main()