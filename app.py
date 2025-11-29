"""
Aplikasi Mesin Pencari Artikel Kesehatan - Modern UI
Support data dari scraping & sample data
"""

import streamlit as st
import pandas as pd
import os
from preprocessor import IndonesianPreprocessor
from vsm import VectorSpaceModel
from bm25 import BM25
from evaluator import IREvaluator
from sample_data import SAMPLE_CORPUS, TEST_QUERIES
from data_loader import DataLoader
import time

# Page config
st.set_page_config(
    page_title="Health Article Search Engine",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with gradient backgrounds and better styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header Styles */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
    }
    
    /* Search Box Styles */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    /* Result Card Styles */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .result-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .result-content {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .result-meta {
        color: #888;
        font-size: 0.85rem;
    }
    
    .result-meta a {
        color: #667eea;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .result-meta a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
    
    /* Badge Styles */
    .score-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .source-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    
    .algorithm-badge {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Sidebar Styles */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .stButton button, [data-testid="stSidebar"] .stButton button {
        background: white;
        color: #667eea;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    
    .css-1d391kg .stButton button:hover, [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.9);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 2px solid transparent;
    }
    
    /* Info Boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Better spacing */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Custom button in main area */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.preprocessor = None
    st.session_state.vsm = None
    st.session_state.bm25 = None
    st.session_state.processed_docs = None
    st.session_state.corpus = None
    st.session_state.data_source = 'sample'

@st.cache_resource
def initialize_system(corpus_data):
    """Initialize preprocessing dan indexing"""
    with st.spinner('🔄 Membangun index dan memuat sistem...'):
        preprocessor = IndonesianPreprocessor()
        processed_docs = preprocessor.preprocess_documents(corpus_data)
        
        vsm = VectorSpaceModel()
        vsm.build_index(processed_docs)
        
        bm25 = BM25(k1=1.5, b=0.75)
        bm25.build_index(processed_docs)
        
    return preprocessor, vsm, bm25, processed_docs

def load_corpus_data():
    """Load corpus data"""
    if os.path.exists('articles_data.json'):
        loader = DataLoader('articles_data.json')
        articles = loader.load_from_json()
        
        if articles and len(articles) > 0:
            return articles, 'scraping'
    
    return SAMPLE_CORPUS, 'sample'

def highlight_keywords(text, keywords, max_length=300):
    """Highlight keywords dalam teks"""
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    for keyword in keywords:
        text = text.replace(keyword, f"**{keyword}**")
    
    return text

def display_results(results, algorithm_name, query_tokens):
    """Display search results with modern styling"""
    st.markdown(f"<div class='algorithm-badge'>{algorithm_name}</div>", unsafe_allow_html=True)
    
    if not results:
        st.info("🔍 Tidak ada hasil yang ditemukan. Coba kata kunci lain.")
        return
    
    for i, result in enumerate(results, 1):
        col1, col2 = st.columns([0.9, 0.1])
        
        with col1:
            st.markdown(f"<div class='result-title'>{i}. {result['title']}</div>", unsafe_allow_html=True)
            
            if 'source' in result and result['source']:
                st.markdown(f"<span class='source-badge'>{result['source']}</span>", unsafe_allow_html=True)
            
            highlighted_content = highlight_keywords(result['content'], query_tokens)
            st.markdown(f"<div class='result-content'>{highlighted_content}</div>", unsafe_allow_html=True)
            
            # Make URL clickable
            st.markdown(
                f"<div class='result-meta'><a href='{result['url']}' target='_blank'>🔗 {result['url']}</a> • 📅 {result['date']}</div>",
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"<div class='score-badge'>{result['score']:.3f}</div>",
                unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)

def run_evaluation():
    """Run evaluation dengan test queries"""
    st.header("📈 Evaluasi Sistem")
    
    preprocessor = st.session_state.preprocessor
    vsm = st.session_state.vsm
    bm25 = st.session_state.bm25
    
    # Check if using scraping data - if yes, re-init with sample data for evaluation
    if st.session_state.data_source == 'scraping':
        with st.spinner('🔄 Mempersiapkan evaluasi dengan sample data...'):
            preprocessor, vsm, bm25, _ = initialize_system(SAMPLE_CORPUS)
    
    evaluator = IREvaluator()
    
    # Add test queries
    for test_query in TEST_QUERIES:
        evaluator.add_test_query(
            test_query['id'],
            test_query['query'],
            test_query['relevant_docs']
        )
    
    # Run evaluation
    with st.spinner('⚡ Menjalankan evaluasi...'):
        vsm_results_by_query = {}
        bm25_results_by_query = {}
        
        for test_query in TEST_QUERIES:
            query_tokens = preprocessor.preprocess(test_query['query'])
            
            # VSM search
            vsm_results = vsm.search(query_tokens, top_k=10)
            vsm_results_by_query[test_query['id']] = vsm_results
            
            # BM25 search
            bm25_results = bm25.search(query_tokens, top_k=10)
            bm25_results_by_query[test_query['id']] = bm25_results
        
        # Evaluate
        vsm_metrics, _ = evaluator.evaluate_system(vsm_results_by_query, k=10)
        bm25_metrics, _ = evaluator.evaluate_system(bm25_results_by_query, k=10)
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔵 Vector Space Model (TF-IDF)")
        metrics_df = pd.DataFrame([vsm_metrics]).T
        metrics_df.columns = ['Score']
        st.dataframe(metrics_df, use_container_width=True)
        
        st.metric("Precision", f"{vsm_metrics['precision']:.4f}")
        st.metric("Recall", f"{vsm_metrics['recall']:.4f}")
        st.metric("F1-Score", f"{vsm_metrics['f1_score']:.4f}")
        st.metric("MAP", f"{vsm_metrics['MAP']:.4f}")
    
    with col2:
        st.subheader("🟢 BM25")
        metrics_df = pd.DataFrame([bm25_metrics]).T
        metrics_df.columns = ['Score']
        st.dataframe(metrics_df, use_container_width=True)
        
        st.metric("Precision", f"{bm25_metrics['precision']:.4f}")
        st.metric("Recall", f"{bm25_metrics['recall']:.4f}")
        st.metric("F1-Score", f"{bm25_metrics['f1_score']:.4f}")
        st.metric("MAP", f"{bm25_metrics['MAP']:.4f}")
    
    # Comparison chart
    st.subheader("📊 Perbandingan Algoritma")
    comparison_df = pd.DataFrame({
        'VSM (TF-IDF)': [
            vsm_metrics['precision'],
            vsm_metrics['recall'],
            vsm_metrics['f1_score'],
            vsm_metrics['MAP']
        ],
        'BM25': [
            bm25_metrics['precision'],
            bm25_metrics['recall'],
            bm25_metrics['f1_score'],
            bm25_metrics['MAP']
        ]
    }, index=['Precision', 'Recall', 'F1-Score', 'MAP'])
    
    st.bar_chart(comparison_df)
    
    # Interpretation
    st.subheader("📝 Interpretasi Hasil")
    
    if vsm_metrics['MAP'] > bm25_metrics['MAP']:
        winner = "Vector Space Model (TF-IDF)"
        winner_map = vsm_metrics['MAP']
    else:
        winner = "BM25"
        winner_map = bm25_metrics['MAP']
    
    st.info(f"""
    **Kesimpulan:** {winner} menunjukkan performa lebih baik dengan MAP {winner_map:.4f}.
    
    - **Precision** mengukur akurasi hasil pencarian (seberapa banyak hasil relevan dari total hasil)
    - **Recall** mengukur kelengkapan hasil (seberapa banyak dokumen relevan yang ditemukan)
    - **F1-Score** adalah harmonic mean dari precision dan recall
    - **MAP (Mean Average Precision)** mengukur performa keseluruhan sistem
    """)

def main():
    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>🏥 Health Article Search Engine</div>
        <div class='hero-subtitle'>Powered by Vector Space Model & BM25 Algorithm</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Pengaturan")
        
        # Data source info
        if os.path.exists('articles_data.json'):
            loader = DataLoader('articles_data.json')
            articles = loader.load_from_json()
            if articles:
                st.success(f"📁 Data tersedia: {len(articles)} artikel")
                
                if st.button("📊 Lihat Statistik Data", use_container_width=True):
                    loader.print_statistics()
        else:
            st.warning("⚠️ File articles_data.json tidak ditemukan")
            st.info("Jalankan `python scraper.py` untuk crawling data")
        
        st.divider()
        
        # Initialize system button
        if st.button("🔄 Inisialisasi/Refresh Sistem", use_container_width=True):
            corpus, data_source = load_corpus_data()
            preprocessor, vsm, bm25, processed_docs = initialize_system(corpus)
            
            st.session_state.preprocessor = preprocessor
            st.session_state.vsm = vsm
            st.session_state.bm25 = bm25
            st.session_state.processed_docs = processed_docs
            st.session_state.corpus = corpus
            st.session_state.data_source = data_source
            st.session_state.initialized = True
            
            st.success("✅ Sistem berhasil diinisialisasi!")
            st.rerun()
        
        st.divider()
        
        # Algorithm selection
        st.subheader("Pilih Algoritma")
        algorithm_choice = st.radio(
            "Tampilkan hasil dari:",
            ["Kedua Algoritma", "VSM (TF-IDF)", "BM25"],
            index=0
        )
        
        # Top-K results
        top_k = st.slider("Jumlah hasil (Top-K)", 1, 20, 10)
        
        st.divider()
        
        # Statistics
        if st.session_state.initialized:
            st.subheader("📊 Statistik Korpus")
            st.metric("Jumlah Dokumen", len(st.session_state.corpus))
            
            vsm_stats = st.session_state.vsm.get_stats()
            st.metric("Ukuran Vocabulary", vsm_stats['vocabulary_size'])
            st.metric("Rata-rata Panjang Dokumen", f"{vsm_stats['avg_doc_length']:.1f}")
            
            if st.session_state.data_source == 'scraping':
                st.success("✅ Menggunakan data scraping")
            else:
                st.info("ℹ️ Menggunakan sample data")
    
    # Main content
    if not st.session_state.initialized:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("### 1️⃣ Setup\nKlik **Mulai Sistem** di sidebar")
        
        with col2:
            st.info("### 2️⃣ Search\nCari artikel kesehatan")
        
        with col3:
            st.info("### 3️⃣ Evaluate\nBandingkan algoritma")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("### 💡 Tentang Aplikasi")
        st.markdown("""
        Aplikasi ini menggunakan dua algoritma pencarian:
        - **VSM (TF-IDF)**: Mengukur kepentingan kata dalam dokumen
        - **BM25**: Algoritma probabilistik yang lebih advanced
        
        Anda dapat membandingkan kedua algoritma untuk melihat mana yang memberikan hasil lebih baik!
        """)
        
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Pencarian", "📈 Evaluasi", "📚 Browse Data"])
    
    with tab1:
        # Search interface
        st.markdown("### 🔍 Cari Artikel Kesehatan")
        
        query = st.text_input(
            "Masukkan kata kunci pencarian:",
            placeholder="Contoh: cara mencegah diabetes, gejala hipertensi, dll."
        )
        
        col1, col2 = st.columns([0.2, 0.8])
        with col1:
            search_button = st.button("🔎 Cari", use_container_width=True)
        
        if search_button and query:
            query_tokens = st.session_state.preprocessor.preprocess(query)
            
            if not query_tokens:
                st.warning("⚠️ Tidak ada token valid setelah preprocessing. Coba kata kunci lain.")
                return
            
            st.info(f"**Query tokens:** {', '.join(query_tokens)}")
            
            # Perform search
            if algorithm_choice in ["Kedua Algoritma", "VSM (TF-IDF)"]:
                start_time = time.time()
                vsm_results = st.session_state.vsm.search(query_tokens, top_k=top_k)
                vsm_time = time.time() - start_time
            
            if algorithm_choice in ["Kedua Algoritma", "BM25"]:
                start_time = time.time()
                bm25_results = st.session_state.bm25.search(query_tokens, top_k=top_k)
                bm25_time = time.time() - start_time
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display results
            if algorithm_choice == "Kedua Algoritma":
                col1, col2 = st.columns(2)
                
                with col1:
                    display_results(vsm_results, "VSM (TF-IDF)", query_tokens)
                    st.caption(f"⏱️ Waktu pencarian: {vsm_time:.4f} detik")
                
                with col2:
                    display_results(bm25_results, "BM25", query_tokens)
                    st.caption(f"⏱️ Waktu pencarian: {bm25_time:.4f} detik")
            
            elif algorithm_choice == "VSM (TF-IDF)":
                display_results(vsm_results, "VSM (TF-IDF)", query_tokens)
                st.caption(f"⏱️ Waktu pencarian: {vsm_time:.4f} detik")
            
            else:
                display_results(bm25_results, "BM25", query_tokens)
                st.caption(f"⏱️ Waktu pencarian: {bm25_time:.4f} detik")
    
    with tab2:
        if st.button("▶️ Jalankan Evaluasi", use_container_width=True):
            run_evaluation()
        else:
            st.info("Klik tombol di atas untuk menjalankan evaluasi sistem dengan test queries.")
            
            # Show test queries
            st.subheader("🧪 Test Queries yang Tersedia")
            for tq in TEST_QUERIES:
                st.write(f"- **{tq['query']}** (Relevan: {len(tq['relevant_docs'])} dokumen)")
    
    with tab3:
        st.subheader("📚 Browse Artikel dalam Dataset")
        
        # Pagination
        items_per_page = 10
        total_items = len(st.session_state.corpus)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        
        page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        
        st.info(f"Menampilkan artikel {start_idx + 1} - {end_idx} dari {total_items}")
        
        for doc in st.session_state.corpus[start_idx:end_idx]:
            with st.expander(f"📄 [{doc['id']}] {doc['title']}"):
                if 'source' in doc:
                    st.markdown(f"**Sumber:** {doc['source']}")
                # Make URL clickable
                st.markdown(f"**URL:** [{doc['url']}]({doc['url']})")
                st.markdown(f"**Tanggal:** {doc['date']}")
                st.divider()
                st.write(doc['content'][:500] + "...")

if __name__ == "__main__":
    main()