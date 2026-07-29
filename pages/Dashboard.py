import streamlit as st
import pandas as pd
import os
import plotly.express as px

# =====================================================================
# 1. KONFIGURASI HALAMAN & STYLE CSS 
# =====================================================================
st.set_page_config(
    page_title="SciClassify - Executive Dashboard",
    page_icon="📊",
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
    
    .dashboard-header {
        background: linear-gradient(135deg, #0f4c81 0%, #1d70b8 100%);
        padding: 30px 40px;
        border-radius: 24px;
        color: white !important;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(15, 76, 129, 0.1);
    }
    
    /* --- STYLE KOTAK METRIK CUSTOM (HTML) --- */
    .metric-container {
        display: flex;
        gap: 15px;
        justify-content: space-between;
        margin-bottom: 30px;
    }
    
    .custom-metric-box {
        flex: 1;
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 16px;
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 4px 12px rgba(148, 163, 184, 0.08);
        text-align: left;
    }
    
    .metric-val {
        color: #0f4c81 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    .metric-lbl {
        color: #1e293b !important; /* Paksa hitam pekat */
        font-size: 13.5px !important;
        font-weight: 700 !important;
        margin-top: 8px !important;
        margin-bottom: 0 !important;
        line-height: 1.4 !important;
    }
    
    .chart-card {
        background-color: #ffffff !important;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 20px rgba(148, 163, 184, 0.05);
        margin-bottom: 25px;
    }
    
    .no-data-card {
        background: #ffffff;
        padding: 50px;
        border-radius: 16px;
        border: 1px dashed #cbd5e1;
        text-align: center;
        color: #64748b;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. HEADER HALAMAN
# =====================================================================
st.markdown("""
    <div class="dashboard-header">
        <h2 style='margin:0; font-weight:800; font-size:28px; letter-spacing: 0.5px;'>📊 Eksekutif Dashboard Analisis</h2>
        <p style='margin:8px 0 0 0; opacity:0.9; font-size:14.5px; line-height:1.5;'>Rangkuman statistik interaktif dan distribusi data hasil klasifikasi teks artikel ilmiah.</p>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 3. LOGIKA BACA & OLAH DATA CSV
# =====================================================================
csv_file = "history.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    
    if not df.empty:
        total_records = len(df)
        category_counts = df["Hasil Kategori"].value_counts()
        
        count_cs = category_counts.get("COMPUTER SCIENCE", 0)
        count_medical = category_counts.get("MEDICAL", 0)
        count_economy = category_counts.get("ECONOMY", 0)
        
        top_category = category_counts.idxmax() if total_records > 0 else "-"
        top_category_clean = top_category.title().replace("Cs", "CS")
        
        # --- BARIS 1: KOTAK METRIK DENGAN HTML ---
        st.markdown("### 📌 Ikhtisar Sistem & Data Konten")
        
        st.markdown(f"""
            <div class="metric-container">
                <div class="custom-metric-box">
                    <p class="metric-val">{total_records} Dok</p>
                    <p class="metric-lbl">📂 Total Dokumen<br><span style='font-weight:500; font-size:12px; color:#64748b;'>(Semua Kategori)</span></p>
                </div>
                <div class="custom-metric-box">
                    <p class="metric-val" style="color: #d97706 !important;">{top_category_clean}</p>
                    <p class="metric-lbl">🏆 Kategori Terbanyak<br><span style='font-weight:500; font-size:12px; color:#64748b;'>(Paling Dominan)</span></p>
                </div>
                <div class="custom-metric-box" style="border-left: 5px solid #1e40af !important;">
                    <p class="metric-val">{count_cs} Dok</p>
                    <p class="metric-lbl">💻 Computer Science<br><span style='font-weight:500; font-size:12px; color:#64748b;'>(Total Artikel CS)</span></p>
                </div>
                <div class="custom-metric-box" style="border-left: 5px solid #166534 !important;">
                    <p class="metric-val">{count_medical} Dok</p>
                    <p class="metric-lbl">🏥 Medical / Kesehatan<br><span style='font-weight:500; font-size:12px; color:#64748b;'>(Total Artikel Medis)</span></p>
                </div>
                <div class="custom-metric-box" style="border-left: 5px solid #d97706 !important;">
                    <p class="metric-val">{count_economy} Dok</p>
                    <p class="metric-lbl">📈 Economy / Ekonomi<br><span style='font-weight:500; font-size:12px; color:#64748b;'>(Total Artikel Ekonomi)</span></p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # --- BARIS 2: GRAFIK DISTRIBUSI (BAR & PIE CHART BERSANDINGAN) ---
        st.markdown("### 📈 Perbandingan Jumlah Kategori")
        df_chart = pd.DataFrame({
            "Kategori": ["Computer Science", "Medical", "Economy"],
            "Jumlah Dokumen": [count_cs, count_medical, count_economy]
        })
        
        color_map = {
            "Computer Science": "#1e40af", 
            "Medical": "#166534", 
            "Economy": "#d97706"
        }
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("<p style='font-weight:700; color:#0f4c81; margin-bottom:15px;'>Volume Dokumen per Kategori (Bar Chart)</p>", unsafe_allow_html=True)
            fig_bar = px.bar(
                df_chart, x="Kategori", y="Jumlah Dokumen", color="Kategori",
                color_discrete_map=color_map, text="Jumlah Dokumen"
            )
            fig_bar.update_traces(textposition='outside', cliponaxis=False, hovertemplate="<b>%{x}</b><br>Total: %{y} Dokumen<extra></extra>")
            fig_bar.update_layout(
                font_family="Plus Jakarta Sans", 
                font_color="#1e293b", 
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False, margin=dict(l=10, r=10, t=30, b=10),
                xaxis=dict(title="", showgrid=False, tickfont=dict(color="#1e293b", size=12)),
                yaxis=dict(title="", showgrid=True, gridcolor="#e2e8f0", tickfont=dict(color="#1e293b"))
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("<p style='font-weight:700; color:#0f4c81; margin-bottom:15px;'>Persentase Proporsi Kategori (Pie Chart)</p>", unsafe_allow_html=True)
            fig_pie = px.pie(
                df_chart, names="Kategori", values="Jumlah Dokumen",
                color="Kategori", color_discrete_map=color_map, hole=0.4
            )
            fig_pie.update_traces(textinfo='percent+label', insidetextorientation='horizontal', hovertemplate="<b>%{label}</b><br>Jumlah: %{value} Dokumen (%{percent})<extra></extra>")
            fig_pie.update_layout(
                font_family="Plus Jakarta Sans", 
                font_color="#1e293b", 
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False, margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Seluruh statistik di atas ditarik langsung dari file history.csv secara real-time.")
        
    else:
        st.markdown('<div class="no-data-card"><h3>📭 Data Grafik Belum Tersedia</h3><p>Silakan lakukan klasifikasi di halaman utama terlebih dahulu untuk memunculkan visualisasi statistik.</p></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="no-data-card"><h3>📭 Data Grafik Belum Tersedia</h3><p>Silakan lakukan klasifikasi di halaman utama terlebih dahulu untuk memunculkan visualisasi statistik.</p></div>', unsafe_allow_html=True)