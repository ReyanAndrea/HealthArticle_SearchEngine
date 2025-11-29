# 🏥 Health Article Search Engine


**Mesin Pencari Artikel Kesehatan Berbahasa Indonesia**

Implementasi Vector Space Model (TF-IDF) dan BM25 untuk Information Retrieval

---

## 📖 Tentang Proyek

Proyek ini adalah implementasi sistem Information Retrieval untuk artikel kesehatan berbahasa Indonesia. Sistem menggunakan dua algoritma ranking yang berbeda untuk memberikan hasil pencarian yang relevan:

- **Vector Space Model (VSM)** dengan pembobotan TF-IDF
- **BM25** (Best Matching 25) - algoritma probabilistic ranking

Proyek ini dikembangkan untuk project UAS dari mata kuliah **Penelusuran Informasi** di Departemen Informatika, Universitas Syiah Kuala.

## ✨ Fitur Utama

### 🔍 Pencarian Multi-Algoritma
- Perbandingan hasil antara VSM (TF-IDF) dan BM25
- Real-time search dengan keyword highlighting
- Ranking berdasarkan score relevansi
- Support untuk query bahasa Indonesia

### 🧹 Text Preprocessing
- **Case Folding** - Normalisasi huruf besar/kecil
- **Tokenization** - Pemecahan teks menjadi token
- **Stopword Removal** - Filter kata umum bahasa Indonesia
- **Stemming** - Menggunakan Sastrawi untuk bahasa Indonesia

### 📊 Evaluasi Sistem
- **Precision** - Akurasi hasil pencarian
- **Recall** - Kelengkapan hasil pencarian
- **F1-Score** - Harmonic mean precision & recall
- **MAP** - Mean Average Precision
- Visualisasi perbandingan performa algoritma

### 🎨 User Interface Modern
- Desain modern dengan gradient colors
- Responsive layout
- Dark mode friendly
- Interactive search results
- Real-time query processing

## 🎯 Demo


**Dashboard Utama**
```
🏥 Health Article Search Engine
Powered by Vector Space Model & BM25 Algorithm
```

**Hasil Pencarian**
- Side-by-side comparison
- Keyword highlighting
- Relevance scores
- Article metadata

**Evaluasi Performa**
- Metric cards
- Comparison charts
- Statistical analysis

## 🚀 Instalasi

### Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Git

### Langkah Instalasi

1. **Clone Repository**
```bash
git clone https://github.com/ReyanAndrea/HealthArticle-SearchEngine.git
cd HealthArticle-SearchEngine
```

2. **Buat Virtual Environment (Recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK Data**
```bash
python -c "import nltk; nltk.download('punkt')"
```

5. **Jalankan Aplikasi**
```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser

## 📁 Struktur Proyek

```
HealthArticle-SearchEngine/
│
├── app.py                      # Main Streamlit application
├── preprocessor.py             # Text preprocessing module
├── vsm.py                      # Vector Space Model implementation
├── bm25.py                     # BM25 algorithm implementation
├── evaluator.py                # Evaluation metrics module
├── sample_data.py              # Sample corpus and test queries
├── data_loader.py              # Data loading utilities
├── scraper.py                  # Web scraping module (optional)
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore rules
```

## 💻 Cara Penggunaan

### 1. Inisialisasi Sistem

- Buka aplikasi di browser
- Klik tombol **"Inisialisasi/Refresh Sistem"** di sidebar
- Tunggu proses indexing selesai

### 2. Melakukan Pencarian

```python
# Contoh query:
- "cara mencegah diabetes"
- "gejala hipertensi"
- "makanan sehat untuk jantung"
- "olahraga menurunkan kolesterol"
```

- Masukkan query di search box
- Pilih algoritma (Kedua/VSM/BM25)
- Klik **"Cari"**
- Lihat hasil dengan score relevansi

### 3. Evaluasi Sistem

- Buka tab **"Evaluasi"**
- Klik **"Jalankan Evaluasi"**
- Analisis performa kedua algoritma
- Bandingkan metrics (Precision, Recall, F1, MAP)

### 4. Browse Dataset

- Buka tab **"Browse Data"**
- Navigasi menggunakan pagination
- Lihat detail setiap artikel

## 🔧 Konfigurasi

### Mengubah Parameter BM25

Edit `app.py` atau `bm25.py`:

```python
bm25 = BM25(
    k1=1.5,    # Term frequency saturation (default: 1.5)
    b=0.75     # Document length normalization (default: 0.75)
)
```

### Menambah Data Corpus

Edit `sample_data.py`:

```python
SAMPLE_CORPUS.append({
    "id": 11,
    "title": "Judul Artikel Baru",
    "content": "Konten artikel kesehatan...",
    "url": "https://example.com/artikel",
    "date": "2024-01-15",
    "source": "Sumber Artikel"
})
```

### Menambah Test Query

Edit `sample_data.py`:

```python
TEST_QUERIES.append({
    "id": "q11",
    "query": "query baru untuk testing",
    "relevant_docs": [1, 3, 5]  # ID dokumen relevan
})
```

## 📊 Algoritma

### Vector Space Model (TF-IDF)

**TF (Term Frequency):**
```
TF(t,d) = count(t,d) / total_terms(d)
```

**IDF (Inverse Document Frequency):**
```
IDF(t) = log(N / df(t))
```

**TF-IDF Weight:**
```
W(t,d) = TF(t,d) × IDF(t)
```

**Cosine Similarity:**
```
sim(q,d) = (q · d) / (||q|| × ||d||)
```

### BM25

**Formula:**
```
score(q,d) = Σ IDF(qi) × [f(qi,d) × (k1 + 1)] / [f(qi,d) + k1 × (1 - b + b × |d|/avgdl)]
```

Dimana:
- `f(qi,d)` = frequency of term qi in document d
- `|d|` = length of document d
- `avgdl` = average document length
- `k1` = term frequency saturation parameter (1.5)
- `b` = length normalization parameter (0.75)

## 📈 Evaluasi Metrics

| Metric | Formula | Deskripsi |
|--------|---------|-----------|
| **Precision** | TP / (TP + FP) | Proporsi dokumen relevan dari hasil |
| **Recall** | TP / (TP + FN) | Proporsi dokumen relevan yang ditemukan |
| **F1-Score** | 2 × (P × R) / (P + R) | Harmonic mean precision & recall |
| **MAP** | Average of AP across queries | Overall system performance |


### Web Scraping (Optional)

Untuk mengumpulkan data artikel kesehatan:

```bash
python scraper.py
```

Script akan crawl artikel dari sumber-sumber kesehatan terpercaya dan menyimpan ke `articles_data.json`.


## 📚 Referensi

1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.

2. Robertson, S., & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond*. Foundations and Trends in Information Retrieval.

3. Salton, G., & Buckley, C. (1988). *Term-weighting Approaches in Automatic Text Retrieval*. Information Processing & Management.

4. Adriani, M., et al. (2007). *Stemming Indonesian: A Confix-Stripping Approach*. ACM Transactions on Asian Language Information Processing.

## 👥 Tim Pengembang

<table>
  <tr>
    <td align="center">
      <img src="https://via.placeholder.com/100" width="100px;" alt=""/><br />
      <sub><b>Reyan Andrea</b></sub><br />
      <sub>2208107010014</sub>
    </td>
    <td align="center">
      <img src="https://via.placeholder.com/100" width="100px;" alt=""/><br />
      <sub><b>Mahardika Shiddiq Anshari</b></sub><br />
      <sub>2308107010032</sub>
    </td>
    <td align="center">
      <img src="https://via.placeholder.com/100" width="100px;" alt=""/><br />
      <sub><b>Muhammad Nazlul Ramadhyan</b></sub><br />
      <sub>2308107010036</sub>
    </td>
  </tr>
</table>

**Departemen Informatika**  
Fakultas Matematika dan Ilmu Pengetahuan Alam  
Universitas Syiah Kuala  
2025

## 🎓 Acknowledgments

Proyek ini dikembangkan sebagai tugas akhir mata kuliah **Penelusuran Informasi** dibawah bimbingan:


## ⭐ Show Your Support

Jika proyek ini membantu Anda, berikan ⭐️ di repository ini!

---

<div align="center">

**Made with ❤️ by kelompok 9 - Universitas Syiah Kuala**

[⬆ Back to Top](#-health-article-search-engine)

</div>
