import streamlit as st
import base64
import os

# =====================================================================
# 1. KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="SciClassify - Home",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk membaca file gambar lokal dan mengubahnya ke Base64 agar bisa dibaca HTML
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Mengambil base64 dari logo lokal kamu (assets/logo.png)
logo_base64 = get_base64_image("assets/logo.png")

# Kustomisasi CSS Premium (Perbaikan Kontras Menu Sidebar)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');
    
    /* --- FORCE HEADER BAR PALING ATAS JADI TERANG --- */
    [data-testid="stHeader"] {
        background-color: #f8fafc !important;
        background: #f8fafc !important;
    }
    
    [data-testid="stHeader"] button, [data-testid="stHeader"] a, [data-testid="stHeader"] span {
        color: #1e293b !important;
    }
    
    /* --- MENYELARASKAN LATAR BELAKANG UTAMA & SIDEBAR --- */
    html, body, [data-testid="stWidgetFormContainer"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc !important;
        color: #1e293b !important;
    }
    
    /* --- SIDEBAR CUSTOMIZATION --- */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* SOLUSI UTAMA: Paksa teks pilihan menu navigasi Streamlit agar berwarna gelap & kelihatan */
    [data-testid="stSidebarNav"] ul li div a span {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Gaya ketika menu navigasi aktif atau di-hover */
    [data-testid="stSidebarNav"] ul li div a:hover {
        background-color: #f1f5f9 !important;
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #334155 !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* --- CSS OVERLAPPING LOGO & BANNER --- */
    .hero-wrapper {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 45px;
        width: 100%;
        padding-left: 10px;
        position: relative;
    }
    
    .logo-container {
        flex-shrink: 0;
        margin-right: -45px;
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .logo-container img {
        width: 200px;
        height: 200px;
        object-fit: cover;
        border-radius: 50%;
        border: 7px solid #ffffff;
        box-shadow: 0 8px 24px rgba(15, 76, 129, 0.15);
        background-color: #ffffff;
    }
    
    .blue-banner {
        flex-grow: 1;
        background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%);
        padding: 30px 40px 30px 75px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(15, 76, 129, 0.15);
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 170px;
        box-sizing: border-box;
        z-index: 1;
    }
    
    .banner-title {
        font-size: 58px; 
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0 0 2px 0 !important;
        color: #ffffff !important;
        line-height: 1;
    }
    
    .banner-subtitle {
        font-size: 15px; 
        font-weight: 700;
        color: #e0f2fe !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 0 !important;
        opacity: 0.95;
    }

    /* --- TEKS UCAPAN SELAMAT DATANG --- */
    .welcome-title {
        text-align: center; 
        font-weight: 800; 
        color: #1e293b !important;
        margin-top: 35px;
        margin-bottom: 6px;
    }
    
    .welcome-desc {
        text-align: center; 
        color: #64748b !important;
        font-size: 15px; 
        margin-bottom: 40px;
    }
    
    /* --- KARTU INFORMASI 3 KOLOM --- */
    .aesthetic-card {
        background: #ffffff !important;
        padding: 28px 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(148, 163, 184, 0.08) !important;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .aesthetic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(148, 163, 184, 0.15) !important;
        border-color: #cbd5e1 !important;
    }
    
    /* --- BANNER AJAKAN CTA --- */
    .aesthetic-cta {
        background: #ffffff !important;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-top: 45px;
        margin-bottom: 25px;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(148, 163, 184, 0.06) !important;
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
        transform: scale(1.03) !important;
        box-shadow: 0 6px 20px rgba(29, 112, 184, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)


# =====================================================================
# 2. SIDEBAR SEBELAH KIRI
# =====================================================================
with st.sidebar:
    st.markdown("<br><hr style='margin: 10px 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color:#ffffff; padding:16px; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'>
        <b style='color:#0f4c81; font-size:15px;'>SciClassify</b><br>
        <span style='font-size:12px; color:#64748b; line-height:1.5; display:inline-block; margin-top:4px;'>
            AI-Powered platform for scientific article classification using machine learning.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-weight:700; font-size:13px; color:#64748b; letter-spacing:1px; margin-bottom:12px;'>📊 STATISTICS</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color:#ffffff; padding:12px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px; display:flex; align-items:center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'>
        <div style='background-color:#0f4c81; color:white; padding:6px 12px; border-radius:8px; font-weight:700; margin-right:12px;'>3</div>
        <div style='font-size:12px;'><b style='color:#1e293b;'>Categories</b><br><span style='color:#64748b;'>Available</span></div>
    </div>
    <div style='background-color:#ffffff; padding:12px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px; display:flex; align-items:center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'>
        <div style='background-color:#8b5cf6; color:white; padding:6px 10px; border-radius:8px; font-weight:700; margin-right:12px;'>AI</div>
        <div style='font-size:12px;'><b style='color:#1e293b;'>Model</b><br><span style='color:#64748b;'>SVM Classifier</span></div>
    </div>
    <div style='background-color:#ffffff; padding:12px; border-radius:10px; border:1px solid #e2e8f0; display:flex; align-items:center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'>
        <div style='background-color:#10b981; color:white; padding:6px 8px; border-radius:8px; font-weight:700; margin-right:12px; font-size:11px;'>PDF</div>
        <div style='font-size:12px;'><b style='color:#1e293b;'>Support</b><br><span style='color:#64748b;'>PDF & Text</span></div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# 3. HALAMAN UTAMA SEBELAH KANAN (KONTEN UTAMA)
# =====================================================================
if logo_base64:
    hero_html = f'<div class="hero-wrapper"><div class="logo-container"><img src="data:image/png;base64,{logo_base64}"></div><div class="blue-banner"><p class="banner-title">SCICLASSIFY</p><p class="banner-subtitle">SCIENTIFIC ARTICLE CLASSIFICATION PLATFORM</p></div></div>'
else:
    hero_html = '<div class="hero-wrapper"><div class="logo-container"><h1 style="font-size: 70px; margin: 0; background-color: white; border-radius: 50%; padding: 20px; border: 7px solid white;">🔬</h1></div><div class="blue-banner"><p class="banner-title">SCICLASSIFY</p><p class="banner-subtitle">SCIENTIFIC ARTICLE CLASSIFICATION PLATFORM</p></div></div>'

st.markdown(hero_html, unsafe_allow_html=True)

# --- TEKS SELAMAT DATANG ---
st.markdown("<h2 class='welcome-title'>Selamat datang di SciClassify! 👋</h2>", unsafe_allow_html=True)
st.markdown("<p class='welcome-desc'>Platform cerdas untuk klasifikasi artikel ilmiah menggunakan machine learning.</p>", unsafe_allow_html=True)

# --- STRUKTUR 3 KATEGORI UTAMA ---
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
    <div class="aesthetic-card">
        <h4 style="color:#0f4c81; font-weight:700; margin-top:0; margin-bottom:12px; font-size:17px;">📚 3 Kategori Utama</h4>
        <p style="font-size:14px; color:#475569; line-height:1.6; margin:0;">
            Sistem dapat mengenali dan mengelompokkan artikel ke dalam 3 bidang besar secara otomatis: 
            <span style="color:#0f4c81; font-weight:600;">Computer Science</span>, <span style="color:#0f4c81; font-weight:600;">Economy</span>, dan <span style="color:#0f4c81; font-weight:600;">Medical</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div class="aesthetic-card">
        <h4 style="color:#7c3aed; font-weight:700; margin-top:0; margin-bottom:12px; font-size:17px;">🤖 Model SVM</h4>
        <p style="font-size:14px; color:#475569; line-height:1.6; margin:0;">
            Proses pemodelan klasifikasi didukung penuh oleh arsitektur algoritma 
            <span style="color:#7c3aed; font-weight:600;">Support Vector Machine (SVM)</span> yang dikombinasikan dengan pembobotan fitur kata <span style="color:#7c3aed; font-weight:600;">TF-IDF</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown("""
    <div class="aesthetic-card">
        <h4 style="color:#059669; font-weight:700; margin-top:0; margin-bottom:12px; font-size:17px;">📝 Teks & Upload PDF</h4>
        <p style="font-size:14px; color:#475569; line-height:1.6; margin:0;">
            Fleksibilitas penuh dalam pengujian dokumen. Bisa langsung <span style="color:#059669; font-weight:600;">menempelkan abstrak teks</span> artikel atau langsung <span style="color:#059669; font-weight:600;">mengunggah dokumen PDF</span>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION BANNER CTA ---
st.markdown("""
    <div class="aesthetic-cta">
        <h3 style="margin:0 0 8px 0; font-weight:700; color:#0f4c81; font-size:22px;">Siap untuk mengklasifikasikan artikel ilmiah?</h3>
        <p style="margin:0 0 0px 0; color:#64748b; font-size:14.5px;">Mulai sekarang untuk mendapatkan hasil klasifikasi yang akurat dan cepat.</p>
    </div>
""", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([2.2, 1, 2.2])
with col_btn2:
    if st.button("Mulai Klasifikasi Artikel", use_container_width=True):
        st.switch_page("pages/Classification.py")

# --- FOOTER HALAMAN ---
st.markdown("<br><br><hr style='border-color: #e2e8f0;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:12px; font-weight:500;'>© 2026 SciClassify. All rights reserved.</p>", unsafe_allow_html=True)