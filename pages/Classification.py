import streamlit as st
import time
import pdfplumber
import pickle
import re
import nltk
import os
import pandas as pd
import sklearn
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# =====================================================================
# 1. OPTIMASI DOWNLOAD RESOURCE NLTK
# =====================================================================
@st.cache_resource
def download_nltk_resources():
    resources = [
        'punkt',
        'punkt_tab',
        'stopwords'
    ]

    for resource in resources:
        try:
            if resource == 'punkt':
                nltk.data.find('tokenizers/punkt')
            elif resource == 'punkt_tab':
                nltk.data.find('tokenizers/punkt_tab')
            elif resource == 'stopwords':
                nltk.data.find('corpora/stopwords')

        except LookupError:
            nltk.download(resource, quiet=True)

download_nltk_resources()

# =====================================================================
# FUNCTION: SIMPAN DATA KE CSV
# =====================================================================
def save_to_csv(text_content, category_result):
    csv_file = "history.csv"
    
    summary_text = text_content.strip().replace("\n", " ")
    if len(summary_text) > 150:
        summary_text = summary_text[:150] + "..."
        
    new_data = {
        "Tanggal/Waktu": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Isi Dokumen / Abstrak": [summary_text],
        "Hasil Kategori": [category_result.upper()]
    }
    new_df = pd.DataFrame(new_data)
    
    if not os.path.exists(csv_file):
        new_df.to_csv(csv_file, index=False)
    else:
        new_df.to_csv(csv_file, mode='a', header=False, index=False)

# =====================================================================
# FUNCTION: MENGAMBIL KEYWORD DENGAN BOBOT TF-IDF TERTINGGI (KATA ASLI / N-GRAM)
# =====================================================================
def extract_keywords_from_model(raw_text, processed_text, tfidf):
    # 1. Transformasi teks input ke representasi vektor TF-IDF
    vector = tfidf.transform([processed_text])
    feature_names = tfidf.get_feature_names_out()
    scores = vector.toarray()[0]

    keyword_scores = []
    for i, score in enumerate(scores):
        if score > 0:
            keyword_scores.append((feature_names[i], score))

    # 2. Urutkan berdasarkan nilai bobot tertinggi
    keyword_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Ambil 8 top stemmed keywords (bisa berupa unigram atau bigram dari model TF-IDF)
    top_stemmed_keywords = [
        word for word, score in keyword_scores[:8]
    ]

    # 3. Proses Anti-Stemming Fleksibel untuk N-Gram
    final_keywords = []

    for stemmed_phrase in top_stemmed_keywords:
        # Pecah frase stem menjadi kata-kata penyusunnya (misal: 'machin learn' -> ['machin', 'learn'])
        stemmed_words = stemmed_phrase.split()
        
        # Susun pola regex dinamis untuk mencari variasi kata asli di raw_text
        regex_patterns = [rf"\b{word}[a-zA-Z]*\b" for word in stemmed_words]
        
        # Menggunakan pembatas fleksibel agar toleran terhadap tanda hubung, tanda baca, atau line-break
        combined_pattern = r".{0,20}?".join(regex_patterns)
        
        # Cari kecocokan substring asli di dalam raw_text dokumen asli (Case-Insensitive)
        match = re.search(combined_pattern, raw_text, re.IGNORECASE)
        
        if match:
            # Jika ditemukan, ambil teks asli dari dokumen dan rapikan formatnya (Capitalize per kata)
            raw_match_text = match.group(0).strip()
            # Bersihkan whitespace berlebih atau karakter aneh hasil tangkapan regex pembatas
            clean_words = re.findall(r'\b[a-zA-Z]+\b', raw_match_text)
            formatted_word = " ".join([w.capitalize() for w in clean_words])
            final_keywords.append(formatted_word)
        else:
            # Jika tidak cocok di dokumen asli, lakukan fallback format huruf kapital standar dari teks stem
            formatted_fallback = " ".join([w.capitalize() for w in stemmed_phrase.split()])
            final_keywords.append(formatted_fallback)

    return final_keywords

# =====================================================================
# 2. KONFIGURASI HALAMAN & STYLE CSS
# =====================================================================
st.set_page_config(
    page_title="SciClassify - Classification",
    page_icon="🔬",
    layout="wide"
)
st.write("Versi sklearn:", sklearn.__version__)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stWidgetFormContainer"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc !important;
        color: #1e293b !important;
    }
    
    div[data-testid="stRadio"] label p {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] {
        background-color: #ffffff !important;
        padding: 10px 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebarNav"] ul li div a span {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stTextArea"] textarea {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
    }

    button[data-baseweb="tab"] p {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #0f4c81 !important;
        font-weight: 700 !important;
    }

    .classify-header {
        background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%);
        padding: 30px 40px;
        border-radius: 24px;
        color: white !important;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(15, 76, 129, 0.1);
    }
    
    .result-card {
        background: #ffffff !important;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(148, 163, 184, 0.08) !important;
        margin-top: 25px;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 14px 40px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(29, 112, 184, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(29, 112, 184, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. LOAD MODEL & VECTORIZER
# =====================================================================
@st.cache_resource
def load_svm_components():
    model = pickle.load(open('model/svm_model.pkl', 'rb'))
    tfidf = pickle.load(open('model/tfidf_vectorizer.pkl', 'rb'))
    return model, tfidf

try:
    model, tfidf = load_svm_components()
except Exception as e:
    st.error(f"Gagal memuat file pkl. Error: {e}")

# =====================================================================
# 4. PIPELINE PREPROCESSING
# =====================================================================
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def pipeline_preprocessing(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text))
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    processed_text = " ".join(tokens)
    return processed_text

def extract_pdf_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        if len(pdf.pages) == 0:
            return ""

        first_page = pdf.pages[0].extract_text()
        if not first_page:
            return ""

        lines = first_page.split("\n")
        title = []
        abstract = []
        found_abstract = False

        stop_words_list = [
            "introduction", "keywords", "index terms", 
            "1 introduction", "i. introduction", "background"
        ]

        ignore_words = [
            "issn", "doi", "received", "accepted", "published", "email", 
            "@", "copyright", "universitas", "journal", "volume", "vol.", "issue"
        ]

        for line in lines:
            text = line.strip()
            if text == "":
                continue

            lower = text.lower()

            if any(word in lower for word in ignore_words):
                continue

            if lower.startswith("abstract"):
                found_abstract = True
                text = re.sub(r'(?i)^abstract[:\s]*', '', text)
                if text != "":
                    abstract.append(text)
                continue

            if found_abstract:
                if any(lower.startswith(word) for word in stop_words_list):
                    break
                abstract.append(text)
            else:
                if len(text) > 15:
                    title.append(text)

        result = " ".join(title + abstract)
        return result

# =====================================================================
# 5. TAMPILAN HEADER & INPUT TABS
# =====================================================================
st.markdown("""
    <div class="classify-header">
        <h2 style='margin:0; font-weight:800; font-size:28px; letter-spacing: 0.5px;'>🔬 Klasifikasi Artikel Ilmiah</h2>
        <p style='margin:8px 0 0 0; opacity:0.9; font-size:14.5px; line-height:1.5;'>Sistem klasifikasi otomatis berbasis algoritma Support Vector Machine (SVM).</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✍️ Input Teks Abstrak", "📂 Unggah Dokumen PDF"])

text_input = ""
uploaded_file = None

with tab1:
    st.markdown("<p style='font-size:14.5px; font-weight:500; color:#475569; margin-top:15px; margin-bottom:10px;'>Tempelkan bagian Judul + Abstrak artikel ilmiah di bawah ini:</p>", unsafe_allow_html=True)
    text_input = st.text_area(label="Abstrak Teks", placeholder="Contoh: This paper presents a new approach in machine learning...", height=220, label_visibility="collapsed")

with tab2:
    st.markdown("<p style='font-size:14.5px; font-weight:500; color:#475569; margin-top:15px; margin-bottom:10px;'>Unggah file artikel ilmiah berformat PDF:</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(label="Upload PDF File", type=["pdf"], label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
pilihan_sumber = st.radio(
    "Metode input yang ingin diklasifikasi saat ini:",
    ["Gunakan Teks Abstrak (Tab 1)", "Gunakan File PDF (Tab 2)"],
    horizontal=True
)

# =====================================================================
# 6. PROSES EKSEKUSI PREDIKSI MODEL SVM
# =====================================================================
col_btn1, col_btn2, col_btn3 = st.columns([2, 1.2, 2])

with col_btn2:
    btn_classify = st.button("Mulai Klasifikasi ✨", use_container_width=True)

if btn_classify:
    raw_text = ""
    is_valid = False
    
    if "Gunakan Teks Abstrak" in pilihan_sumber:
        if text_input.strip() == "":
            st.error("❌ Kotak input teks abstrak di Tab 1 masih kosong!")
        elif len(text_input.split()) < 5:
            st.error("⚠️ Teks terlalu pendek!")
        else:
            raw_text = text_input
            is_valid = True
            
    elif "Gunakan File PDF" in pilihan_sumber:
        if uploaded_file is None:
            st.error("❌ File PDF di Tab 2 belum diunggah!")
        else:
            raw_text = extract_pdf_text(uploaded_file)
            if len(raw_text.split()) < 5:
                st.error("⚠️ Konten PDF terdeteksi terlalu pendek.")
            else:
                is_valid = True

    if is_valid and raw_text.strip() != "":
        with st.spinner("Sedang memproses teks & melakukan klasifikasi..."):
            time.sleep(0.8)
            
            # Preprocessing teks
            processed_text = pipeline_preprocessing(raw_text)
            text_vector = tfidf.transform([processed_text])
            prediksi_kategori = model.predict(text_vector)[0]
            label_clean = str(prediksi_kategori).lower().strip()
            
            # Mengambil kata kunci asli (bukan stemmed) berdasarkan bobot TF-IDF tertinggi
            keywords = extract_keywords_from_model(
                raw_text,
                processed_text,
                tfidf
            )
            
            # Simpan log ke history file
            save_to_csv(raw_text, prediksi_kategori)
            
            # Penentuan skema warna visual card kategori halaman
            if "medical" in label_clean:
                color_theme = "#f0fdf4"   
                border_theme = "#bbf7d0"
                text_color = "#166534"
            elif "computer science" in label_clean:
                color_theme = "#eff6ff"   
                border_theme = "#bfdbfe"
                text_color = "#1e40af"
            else: # Default (Economy atau Kategori Lainnya)
                color_theme = "#fffbeb"   
                border_theme = "#fef3c7"
                text_color = "#92400e"

            # -----------------------------------------------------------------
            # TAMPILAN UTAMA HASIL KLASIFIKASI (GRID ELEGAN)
            # -----------------------------------------------------------------
            
            # 1. Kita buat list badge dalam satu baris string rapat (tanpa spasi/newline)
            # Ini sangat krusial agar parser Markdown Streamlit tidak menganggapnya teks biasa
            list_badges = []
            for word in keywords:
                list_badges.append(
                    f'<span style="display:inline-block; background-color:#eff6ff !important; border:1px solid #bfdbfe !important; color:#1e40af !important; padding:6px 14px !important; margin:4px !important; border-radius:20px !important; font-size:13px !important; font-weight:600 !important;">✓ {word}</span>'
                )
            keyword_badges = "".join(list_badges)

            joined_words = ", ".join([f"<i>{w}</i>" for w in keywords])
            
            # 2. Gabungkan seluruh HTML menjadi satu string rapat, lalu buang semua baris baru (\n)
            html_output = f"""
            <div class="result-card" style="margin-top: 30px; background: #ffffff; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(148, 163, 184, 0.08);">
                <h3 style="margin:0 0 10px 0; color:#0f4c81; font-weight:700; font-size:20px;">📊 Hasil Klasifikasi</h3>
                <div style="height:1px; background-color:#e2e8f0; margin-bottom:20px;"></div>
                
                <p style="font-size:14px; color:#64748b; margin-bottom:8px; font-weight:500;">Kategori Artikel Ilmiah:</p>
                <div style="background:{color_theme}; padding:12px 24px; border-radius:12px; border:1px solid {border_theme}; display:inline-block; margin-bottom:25px;">
                    <span style="font-size:22px; font-weight:800; color:{text_color}; letter-spacing:0.5px;">🚀 {prediksi_kategori.upper()}</span>
                </div>
                
                <h4 style="margin:0 0 10px 0; color:#1e293b; font-weight:600; font-size:16px;">🔑 Kata Kunci Terdeteksi</h4>
                <div style="display:block; margin-bottom:25px; line-height:1.8;">
                    {keyword_badges if keywords else '<p style="color:#64748b; font-style:italic;">Tidak ada kata kunci signifikan.</p>'}
                </div>
                
                <h4 style="margin:0 0 10px 0; color:#1e293b; font-weight:600; font-size:16px;">💡 Analisis Sistem</h4>
                <div style="background:#f8fafc; border-left:5px solid #0f4c81; padding:16px; border-radius:4px 12px 12px 4px; border-top:1px solid #e2e8f0; border-right:1px solid #e2e8f0; border-bottom:1px solid #e2e8f0; line-height:1.6; color:#475569; font-size:14px; margin-bottom:15px;">
                    Artikel diklasifikasikan sebagai <b>{prediksi_kategori.upper()}</b> berdasarkan pola fitur teks yang dipelajari oleh model SVM melalui representasi TF-IDF. Beberapa kata dengan bobot fitur tertinggi yang ditemukan pada artikel dan mendukung hasil klasifikasi yaitu: {joined_words}.
                </div>
            </div>
            """
            
            # Langkah pamungkas: Hapus jeda enter (\n) agar Markdown Streamlit terpaksa membaca Pure HTML
            clean_html = html_output.replace('\n', ' ').strip()
            
            st.markdown(clean_html, unsafe_allow_html=True)
            
            # Progress Bar Validitas Model
            st.markdown("<br><p style='font-size:14px; margin-bottom:5px; font-weight:600; color:#475569;'>Tingkat Validitas Model:</p>", unsafe_allow_html=True)
            st.progress(0.97)
            st.caption("Hasil pengujian berbasis model SVM dengan performa akurasi sistem pengujian sebesar 97.16%.")
