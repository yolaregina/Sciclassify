import streamlit as st
import pandas as pd
import os
import time

# =====================================================================
# 1. KONFIGURASI HALAMAN & STYLE CSS
# =====================================================================
st.set_page_config(
    page_title="SciClassify - History",
    page_icon="📜",
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
    
    .history-header {
        background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%);
        padding: 30px 40px;
        border-radius: 24px;
        color: white !important;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(15, 76, 129, 0.1);
    }
    
    .no-data-card {
        background: #ffffff;
        padding: 40px;
        border-radius: 16px;
        border: 1px dashed #cbd5e1;
        text-align: center;
        color: #64748b;
        margin-top: 20px;
    }
    
    /* Style custom untuk mempercantik text input pencarian */
    [data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. HEADER HALAMAN
# =====================================================================
st.markdown("""
    <div class="history-header">
        <h2 style='margin:0; font-weight:800; font-size:28px; letter-spacing: 0.5px;'>📜 Riwayat Klasifikasi</h2>
        <p style='margin:8px 0 0 0; opacity:0.9; font-size:14.5px; line-height:1.5;'>Menampilkan seluruh daftar riwayat hasil pengujian artikel ilmiah yang telah tersimpan.</p>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 3. LOGIKA BACA, CARI, & TAMPILKAN DATA CSV
# =====================================================================
csv_file = "history.csv"

if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file)
        
        if not df.empty:
            # Urutkan riwayat dari yang paling baru di posisi atas
            df_reversed = df.iloc[::-1].reset_index(drop=True)
            
            # --- FITUR PENCARIAN ---
            st.markdown("### 🔍 Cari Data Riwayat")
            search_query = st.text_input(
                label="Cari berdasarkan kata kunci teks abstrak atau hasil kategori...",
                placeholder="Ketik kata kunci di sini (contoh: 'machine', 'medical', 'economy')...",
                label_visibility="collapsed"
            )
            
            # Logika Filter Data berdasarkan input pencarian (case-insensitive / tidak sensitif huruf besar-kecil)
            if search_query:
                # Cari kata kunci di kolom abstrak maupun kolom hasil kategori
                filter_abstrak = df_reversed["Isi Dokumen / Abstrak"].astype(str).str.contains(search_query, case=False, na=False)
                filter_kategori = df_reversed["Hasil Kategori"].astype(str).str.contains(search_query, case=False, na=False)
                df_filtered = df_reversed[filter_abstrak | filter_kategori].reset_index(drop=True)
            else:
                df_filtered = df_reversed
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Menampilkan informasi jumlah riwayat yang ditemukan
            if search_query:
                st.markdown(f"🔍 Ditemukan **{len(df_filtered)}** hasil pencarian untuk kata kunci: *'{search_query}'*")
            else:
                st.markdown(f"**Total Riwayat:** {len(df_filtered)} Dokumen telah diperiksa.")
            
            # Menampilkan tabel jika data hasil filter tidak kosong
            if not df_filtered.empty:
                st.dataframe(
                    df_filtered,
                    use_container_width=True,
                    column_config={
                        "Tanggal/Waktu": st.column_config.TextColumn("📅 Waktu Analisis", width="medium"),
                        "Isi Dokumen / Abstrak": st.column_config.TextColumn("📝 Potongan Isi Teks/Abstrak", width="large"),
                        "Hasil Kategori": st.column_config.TextColumn("🚀 Hasil Kategori", width="medium")
                    }
                )
            else:
                st.warning(f"Tidak ada riwayat yang cocok dengan kata kunci '{search_query}'.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Fitur: Tombol Reset / Hapus Seluruh Riwayat CSV
            col1, col2 = st.columns([8, 2])
            with col2:
                if st.button("🗑️ Hapus Semua Riwayat", use_container_width=True):
                    os.remove(csv_file)
                    st.success("Riwayat berhasil dibersihkan!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.markdown('<div class="no-data-card"><h3>📭 Belum Ada Riwayat</h3><p>Silakan lakukan klasifikasi teks atau file PDF terlebih dahulu di halaman utama.</p></div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Gagal membaca file riwayat: {e}")
else:
    st.markdown('<div class="no-data-card"><h3>📭 Belum Ada Riwayat</h3><p>Silakan lakukan klasifikasi teks atau file PDF terlebih dahulu di halaman utama.</p></div>', unsafe_allow_html=True)