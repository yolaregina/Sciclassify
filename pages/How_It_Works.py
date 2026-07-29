import streamlit as st

# =====================================================================
# 1. KONFIGURASI HALAMAN & STYLE CSS (DIPERBAIKI UNTUK METRIC TEXT)
# =====================================================================
st.set_page_config(
    page_title="SciClassify - How It Works",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');
    
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc !important;
        color: #1e293b !important;
    }
    
    /* Perbaikan Khusus agar Tulisan st.metric Kelihatan Jelas */
    div[data-testid="stMetricValue"] {
        color: #0f4c81 !important;
        font-weight: 800 !important;
        font-size: 28px !important;
    }
    
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    div[data-testid="stMetricDelta"] div {
        font-weight: 600 !important;
    }
    
    /* Style Box Card untuk Metrik agar Lebih Cantik */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 10px rgba(148, 163, 184, 0.05);
    }
    
    .header-box {
        background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%);
        padding: 30px 40px;
        border-radius: 24px;
        color: white !important;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(15, 76, 129, 0.1);
    }
    
    .step-card {
        background: #ffffff !important;
        padding: 25px;
        border-radius: 16px;
        border-left: 5px solid #1d70b8;
        box-shadow: 0 4px 15px rgba(148, 163, 184, 0.08) !important;
        margin-bottom: 20px;
    }
    
    .step-number {
        background: #eff6ff;
        color: #0f4c81;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .badge-method {
        background: #f1f5f9;
        color: #334155;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. HEADER HALAMAN
# =====================================================================
st.markdown("""
    <div class="header-box">
        <h2 style='margin:0; font-weight:800; font-size:28px; letter-spacing: 0.5px;'>🧠 Bagaimana Sistem Ini Bekerja?</h2>
        <p style='margin:8px 0 0 0; opacity:0.9; font-size:14.5px; line-height:1.5;'>Pelajari alur pemrosesan data teks dari artikel ilmiah hingga menghasilkan prediksi kategori yang akurat.</p>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 3. ALUR PEMROSESAN (STEP BY STEP)
# =====================================================================
st.markdown("### 📋 Alur Pipa Data (*Text Mining Pipeline*)")
st.write("Aplikasi ini menggunakan pendekatan kecerdasan buatan berbasis *Natural Language Processing* (NLP) dan algoritma *Support Vector Machine* (SVM). Berikut adalah 4 tahapan utamanya:")

# --- STEP 1 ---
st.markdown("""
    <div class="step-card">
        <span class="step-number">Langkah 1</span>
        <h4 style="margin: 5px 0; color: #0f4c81; font-weight:700;">📥 Input Pengumpulan Data (Data Ingestion)</h4>
        <p style="margin: 8px 0; color: #475569; font-size: 14.5px; line-height: 1.6;">
            Pengguna memasukkan data artikel ilmiah melalui dua jalur alternatif: mengetik/menempelkan teks abstrak secara langsung, atau mengunggah dokumen berformat <b>PDF</b>. Jika menggunakan file PDF, sistem akan mengekstrak teks pada halaman awal secara otomatis menggunakan pustaka <i>pdfplumber</i>.
        </p>
        <span class="badge-method">Komponen: Streamlit Text Area & PDF Plumber</span>
    </div>
""", unsafe_allow_html=True)

# --- STEP 2 ---
st.markdown("""
    <div class="step-card" style="border-left-color: #10b981;">
        <span class="step-number" style="background: #ecfdf5; color: #10b981;">Langkah 2</span>
        <h4 style="margin: 5px 0; color: #10b981; font-weight:700;">🧹 Pra-pemrosesan Teks (Text Preprocessing)</h4>
        <p style="margin: 8px 0; color: #475569; font-size: 14.5px; line-height: 1.6;">
            Teks mentah yang masuk disinkronkan dengan standar data training melalui 5 sub-proses NLTK:
        </p>
        <ul style="color: #475569; font-size: 14px; padding-left: 20px;">
            <li><b>Cleaning:</b> Menghapus angka, tanda baca, dan karakter khusus menggunakan <i>Regular Expression (Regex)</i>.</li>
            <li><b>Case Folding:</b> Menyeragamkan seluruh teks menjadi huruf kecil (lowercase).</li>
            <li><b>Tokenizing:</b> Memecah rentetan kalimat abstrak menjadi potongan kata tunggal (token).</li>
            <li><b>Stopword Removal:</b> Membuang kata hubung bahasa Inggris yang tidak membawa makna krusial (seperti: <i>the, and, of, in</i>).</li>
            <li><b>Stemming:</b> Mengubah kata berimbuhan menjadi kata dasarnya menggunakan algoritma <i>Porter Stemmer</i> (contoh: <i>"learning"</i> menjadi <i>"learn"</i>).</li>
        </ul>
        <span class="badge-method">Komponen: NLTK Library (RegEx, Tokenizer, Stopwords, PorterStemmer)</span>
    </div>
""", unsafe_allow_html=True)

# --- STEP 3 ---
st.markdown("""
    <div class="step-card" style="border-left-color: #f59e0b;">
        <span class="step-number" style="background: #fffbeb; color: #f59e0b;">Langkah 3</span>
        <h4 style="margin: 5px 0; color: #f59e0b; font-weight:700;">📊 Ekstraksi Fitur (TF-IDF Vectorization)</h4>
        <p style="margin: 8px 0; color: #475569; font-size: 14.5px; line-height: 1.6;">
            Mesin pintar tidak dapat membaca teks alfabet langsung, sehingga kata dasar hasil pembersihan dikonversi menjadi representasi angka (vektor matriks) menggunakan metode <b>TF-IDF</b> (<i>Term Frequency - Inverse Document Frequency</i>). Proses ini bekerja dengan memberikan bobot nilai pada kata unik yang paling mencerminkan inti konten artikel ilmiah.
        </p>
        <span class="badge-method">Komponen: tfidf_vectorizer.pkl (Scikit-Learn)</span>
    </div>
""", unsafe_allow_html=True)

# --- STEP 4 ---
st.markdown("""
    <div class="step-card" style="border-left-color: #8b5cf6;">
        <span class="step-number" style="background: #f5f3ff; color: #8b5cf6;">Langkah 4</span>
        <h4 style="margin: 5px 0; color: #8b5cf6; font-weight:700;">🚀 Klasifikasi Nyata (SVM Model Prediction)</h4>
        <p style="margin: 8px 0; color: #475569; font-size: 14.5px; line-height: 1.6;">
            Matriks angka dari TF-IDF kemudian diumpankan ke model utama <b>Support Vector Machine (SVM)</b> yang sudah dilatih sebelumnya. Berdasarkan pola batas keputusan (<i>hyperplane</i>) yang optimal, model mengklasifikasikan artikel ilmiah tersebut ke dalam salah satu dari tiga kategori target: <b>Computer Science</b>, <b>Economy</b>, atau <b>Medical</b>.
        </p>
        <span class="badge-method">Komponen: svm_model.pkl (Scikit-Learn)</span>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 4. KINERJA MODEL INFORMASI (FAKTA SIDANG)
# =====================================================================
st.markdown("---")
st.markdown("### 📈 Catatan Akurasi Model Evaluasi")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Akurasi Pengujian Sistem", value="97.16%", delta="Sangat Baik")
with col2:
    st.metric(label="Algoritma Klasifikasi", value="SVM (SVC)", delta="Linear Kernel")
with col3:
    st.metric(label="Target Variabel", value="3 Kategori", delta="CS, Economy, Medical")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Catatan: Performa di atas didapatkan dari hasil pembagian data latih dan data uji pada notebook riset menggunakan skema pembobotan TF-IDF.")