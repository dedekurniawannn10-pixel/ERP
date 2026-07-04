import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
# --- KELOLA FILE DATABASE LOKAL (DENGAN PROTEKSI AUTO-CREATE) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(page_title="Login Sistem", layout="centered")

# 2. CSS injector untuk membersihkan siluet putih & merapikan tombol mata password
st.markdown(f"""
    <style>
    /* Mewarnai area bar atas (Header/Top Bar) agar tidak putih belang */
    header, [data-testid="stHeader"] {{
        background-color: #0f1e36 !important;
    }}
    
    /* Mengubah warna teks/tombol bawaan di header atas (seperti tombol Deploy / Menu) */
    [data-testid="stHeader"] button, [data-testid="stHeader"] a {{
        color: #10b981 !important;
    }}
    
    /* Latar belakang utama seluruh aplikasi */
    .stApp {{
        background-color: #0f1e36;
    }}
    
    /* Kartu/Kotak Login Tengah - dibuat Pop-out proporsional */
    [data-testid="stVerticalBlockBorderContainer"] {{
        background-color: #132644 !important; /* Sedikit lebih terang dari bg utama agar berdimensi */
        border: 1px solid #10b981 !important;
        border-radius: 12px;
        padding: 40px !important;
        max-width: 450px;
        margin: auto;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.4);
    }}
    
    /* Label teks tulisan "Username" & "Password" */
    label {{
        color: #10b981 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 6px;
    }}
    
    /* =======================================================
       PERBAIKAN TOTAL KOTAK INPUT & TOMBOL MATA PASSWORD
       ======================================================= */
       
    /* Memaksa pembungkus luar input box agar berwarna gelap murni & border emerald */
    [data-testid="stTextInputRootElement"] {{
        background-color: #0f1e36 !important;
        border: 1px solid #10b981 !important;
        border-radius: 6px !important;
    }}
    
    /* Membuang semua sisa siluet putih/abu bawaan Streamlit di dalam kotak */
    [data-testid="stTextInputRootElement"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}
    
    /* Mengatur teks input ketikan di dalam kotak */
    .stTextInput input {{
        background-color: transparent !important;
        color: #ffffff !important; /* Teks ketikan warna putih bersih */
        border: none !important;
        font-size: 15px !important;
    }}
    
    /* Warna teks petunjuk (placeholder) di dalam kotak ketik */
    .stTextInput input::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}
    
    /* Memaksa background tombol mata password menjadi transparan/gelap murni */
    [data-testid="stTextInputRootElement"] button {{
        background-color: transparent !important;
        color: #10b981 !important; /* Ikon mata berwarna emerald full */
        border: none !important;
    }}
    
    /* Efek hover pada tombol mata */
    [data-testid="stTextInputRootElement"] button:hover {{
        color: #0d9668 !important;
        background-color: transparent !important;
    }}
    
    /* =======================================================
       KUSTOMISASI TOMBOL 'MASUK' (Penuh & teks di tengah murni)
       ======================================================= */
    div[data-testid="stButton"] {{
        width: 100% !important;
    }}
    
    div[data-testid="stButton"] button {{
        background-color: #10b981 !important;
        color: #0f1e36 !important; /* Teks tombol gelap agar kontras tinggi */
        border: none !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px 0px !important;
        border-radius: 6px !important;
        
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }}
    
    /* Efek saat tombol disentuh mouse (Hover) */
    div[data-testid="stButton"] button:hover {{
        background-color: #0d9668 !important;
        color: #ffffff !important;
    }}
    </style>
""", unsafe_allow_html=True)

def login_form():
    with st.container(border=True):
        
        # Grid kolom untuk menaruh Logo CV GNET tepat di tengah atas kartu
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.image("cvgnet.png", use_container_width=True)
            
        st.write("") # Spasi pemisah objek
        
        # Form Input Fields
        user = st.text_input("Username", placeholder="Masukkan Username Anda")
        pwd = st.text_input("Password", type="password", placeholder="Masukkan Password Anda")
        
        st.write("") # Spasi sebelum tombol
        
        # Tombol Masuk menggunakan parameter use_container_width agar melebar otomatis
        if st.button("Masuk", use_container_width=True):
            if user == "admin" and pwd == "gnet2712": 
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Username/Password salah!")

# Inisialisasi status login (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_form()
    st.stop()

FILE_BARANG = "data_barang.csv"
FILE_MASUK = "barang_masuk.csv"
FILE_KELUAR = "barang_keluar.csv"
FILE_TEKNISI = "teknisi.csv"
FILE_LOG = "log_aktivitas.csv"

if not os.path.exists(FILE_BARANG):
    pd.DataFrame(columns=["Nama Barang", "Stok"]).to_csv(FILE_BARANG, index=False)
if not os.path.exists(FILE_MASUK):
    pd.DataFrame(columns=["Tanggal", "Nama Barang", "Qty", "Keterangan"]).to_csv(FILE_MASUK, index=False)
if not os.path.exists(FILE_KELUAR):
    pd.DataFrame(columns=["Tanggal", "Nama Barang", "Teknisi", "Qty", "Keperluan", "Keterangan"]).to_csv(FILE_KELUAR, index=False)
if not os.path.exists(FILE_TEKNISI):
    pd.DataFrame(columns=["Nama Teknisi"]).to_csv(FILE_TEKNISI, index=False)
if not os.path.exists(FILE_LOG):
    pd.DataFrame(columns=["Waktu", "Aktivitas"]).to_csv(FILE_LOG, index=False)

# Membaca Data
df_barang = pd.read_csv(FILE_BARANG)
df_masuk = pd.read_csv(FILE_MASUK)
df_keluar = pd.read_csv(FILE_KELUAR)
df_teknisi = pd.read_csv(FILE_TEKNISI)
df_log = pd.read_csv(FILE_LOG)

if not df_masuk.empty:
    df_masuk['Tanggal'] = pd.to_datetime(df_masuk['Tanggal'], errors='coerce')
if not df_keluar.empty:
    df_keluar['Tanggal'] = pd.to_datetime(df_keluar['Tanggal'], errors='coerce')

# --- KONFIGURASI HALAMAN WEB ---
st.set_page_config(page_title="Inventory System - CV GNET", layout="wide")


# =============== KONFIGURASI CSS (Sudah Diperbaiki) ===============
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* Base Aplikasi */
        .stApp {
            background-color: #f8fafc !important;
        }
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        div.block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 95% !important;
        }
        div[data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
        }
        
        /* SIDEBAR FIX: Menaikkan posisi logo tanpa merusak layout */
        div[data-testid="stSidebarContent"] {
            padding-top: 1.5rem !important;
        }
        [data-testid="stSidebar"] {
            background-color: #0f1e36 !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
        }

        /* Menghilangkan pembungkus/border bawaan iframe menu option_menu */
        iframe[title="streamlit_option_menu.option_menu"] {
            border: 0px !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        
        /* Header Dashboard - Border Kiri Hijau */
        .page-header-container {
            background-color: #ffffff !important;
            padding: 20px 24px !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05) !important;
            margin-bottom: 24px !important;
            border-left: 5px solid #10b981 !important;
        }
        
        /* Metric Cards */
        .metric-card {
            background: #ffffff !important;
            padding: 24px !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px rgba(15,23,42,0.05) !important;
            border: 1px solid #e2e8f0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
        }
        .metric-icon-box {
            width: 48px !important;
            height: 48px !important;
            border-radius: 10px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 20px !important;
        }
        .metric-title {
            font-size: 14px !important;
            color: #64748b !important;
            font-weight: 500 !important;
            margin-bottom: 4px !important;
        }
        .metric-value {
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            margin: 0 !important;
        }

        /* Balok Header Konten */
        .block-header {
            background-color: #0f1e36 !important; 
            margin: -17px -17px 15px -17px; 
            padding: 14px 18px; 
            border-top-left-radius: 10px; 
            border-top-right-radius: 10px; 
            color: #f8fafc !important; 
            font-weight: 600; 
            font-size: 14px;
            display: flex;
            align-items: center;
        }
        .block-header svg {
            margin-right: 10px !important;
            fill: #10b981 !important;
            flex-shrink: 0;
        }
    </style>
""", unsafe_allow_html=True)


# =============== STRUCTURE SIDEBAR ===============
with st.sidebar:
    # Logo aman di paling atas
    st.image("cvgnet.png", use_container_width=True)
    
    # Pembatas antara logo dan menu
    st.markdown("<hr style='border: 0; height: 1px; background: linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.15), rgba(255,255,255,0)); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Menu Utama
    menu = option_menu(
        menu_title=None, 
        options=["Dashboard", "Manajemen Stok", "Barang Masuk", "Barang Keluar", "Log Book Aktivitas"],
        icons=["bar-chart-fill", "box-seam", "download", "upload", "file-earmark-text"],
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {
                "padding": "0px !important", 
                "background-color": "#0f1e36 !important", 
                "border": "none !important", 
                "box-shadow": "none !important",
                "border-radius": "0px"
            },
            "icon": {"color": "rgba(255, 255, 255, 0.70)", "font-size": "14px"}, 
            "nav-link": {
                "color": "rgba(255, 255, 255, 0.85)", 
                "font-size": "14px", 
                "text-align": "left", 
                "margin": "6px 0px", 
                "padding": "12px 15px",
                "border-radius": "8px",
                "box-shadow": "none !important",
                "outline": "none !important",
                "border": "none !important",
                "--hover-color": "#0a7250"
            },
            "nav-link-selected": {
                "background-color": "#10b981", 
                "color": "#ffffff", 
                "font-weight": "600",
                "border-radius": "8px",
                "box-shadow": "none !important",
                "outline": "none !important",
                "border": "none !important"
            },
        }
    )
    
    # Memberikan spasi kosong yang proporsional di bawah menu sebelum tombol logout
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Tombol Logout menyesuaikan alur posisi menu dengan aman
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# 1. HALAMAN DASHBOARD
# ==========================================
if menu == "Dashboard":
    st.markdown("""
        <div class="page-header-container">
            <h3 class="fw-bold text-dark m-0" style="font-size: 22px;">📊 Dashboard Analitik</h3>
            <p class="text-muted small m-0" style="font-size: 13px; margin-top: 4px !important;">Ringkasan performa dan mutasi logistik perangkat gudang.</p>       
        </div>
    """, unsafe_allow_html=True)
    
    total_unit_fisik = int(df_barang["Stok"].sum()) if not df_barang.empty else 0
    total_tx_masuk = int(df_masuk['Qty'].sum()) if not df_masuk.empty else 0   
    total_tx_keluar = int(df_keluar['Qty'].sum()) if not df_keluar.empty else 0 
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-title">Total Stok Produk</div>
                    <div class="metric-value">{total_unit_fisik}</div>
                </div>
                <div class="metric-icon-box" style="background-color: #e0f2fe; color: #0369a1;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16"><path d="M8.186 1.113a.5.5 0 0 0-.372 0L1.846 3.5 8 5.961 14.154 3.5zM15 4.239l-6.5 2.6v7.922l6.5-2.6V4.24zM7.5 14.762V6.838L1 4.239v5.683zm-1-.239L1 11.923V4.24l5.5 2.2z"/></svg>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-title">Total Transaksi Masuk</div>
                    <div class="metric-value">{total_tx_masuk}</div>
                </div>
                <div class="metric-icon-box" style="background-color: #dcfce7; color: #15803d;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16"><path d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M4.854 8.146a.5.5 0 0 1 .708 0L7.5 10.192V4.5a.5.5 0 0 1 1 0v5.692l1.938-1.938a.5.5 0 1 1 .708.708l-2.793 2.793a.5.5 0 0 1-.707 0L4.854 8.854a.5.5 0 0 1 0-.708"/></svg>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-title">Total Transaksi Keluar</div>
                    <div class="metric-value">{total_tx_keluar}</div>
                </div>
                <div class="metric-icon-box" style="background-color: #fee2e2; color: #b91c1c;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16"><path d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-7.5 3.5a.5.5 0 0 1-1 0V5.808L5.56 7.747a.5.5 0 1 1-.708-.708l2.793-2.793a.5.5 0 0 1 .707 0l2.793 2.793a.5.5 0 1 1-.708.708L8.5 5.808z"/></svg>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    col_grafik1, col_grafik2 = st.columns([1.6, 1.4])
    
    with col_grafik1:
        with st.container(border=True):
            st.markdown("""
                <div class="block-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M0 0h1v15h15v1H0zm10 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V4.707l-5.323 5.323a.5.5 0 0 1-.672.04l-2.436-1.624L1.854 12.146a.5.5 0 1 1-.708-.708l4-4a.5.5 0 0 1 .623-.04l2.436 1.624l4.646-4.646H10.5a.5.5 0 0 1-.5-.5"/></svg>
                    Grafik Tren Transaksi
                </div>
            """, unsafe_allow_html=True)
            
            tipe_tren = st.radio("Rentang Waktu:", ["Bulan", "Hari"], horizontal=True, label_visibility="collapsed")

            if not df_masuk.empty or not df_keluar.empty:
                if tipe_tren == "Bulan":
                    m_data = df_masuk.groupby(df_masuk['Tanggal'].dt.to_period('M'))['Qty'].sum() if not df_masuk.empty else pd.Series()
                    k_data = df_keluar.groupby(df_keluar['Tanggal'].dt.to_period('M'))['Qty'].sum() if not df_keluar.empty else pd.Series()
                    chart_data = pd.DataFrame({'Barang Masuk': m_data, 'Barang Keluar': k_data}).fillna(0)
                    chart_data.index = chart_data.index.to_timestamp()
                else:
                    m_data = df_masuk.groupby(df_masuk['Tanggal'].dt.normalize())['Qty'].sum() if not df_masuk.empty else pd.Series()
                    k_data = df_keluar.groupby(df_keluar['Tanggal'].dt.normalize())['Qty'].sum() if not df_keluar.empty else pd.Series()
                    chart_data = pd.DataFrame({'Barang Masuk': m_data, 'Barang Keluar': k_data}).fillna(0)
                    chart_data.index = pd.to_datetime(chart_data.index)
                
                chart_data = chart_data.sort_index()
                st.line_chart(chart_data, color=["#10b981", "#ef4444"], height=265)
            else:
                st.info("Belum ada data transaksi.")
            
    with col_grafik2:
        with st.container(border=True):
            st.markdown("""
                <div class="block-header">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M15.985 8.5H8.207l-5.5 5.5a8 8 0 0 0 13.277-5.5zM2 13.292A8 8 0 0 1 7.5.015v7.778zM8.5.015V7.5h7.485A8 8 0 0 0 8.5.015"/></svg>
                    Proporsi Distribusi Stok Perangkat
                </div>
            """, unsafe_allow_html=True)
            
            if not df_barang.empty and df_barang["Stok"].sum() > 0:
                import altair as alt
                
                pie_chart = alt.Chart(df_barang).mark_arc(innerRadius=0, stroke="#fff").encode(
                    theta=alt.Theta(field="Stok", type="quantitative"),
                    color=alt.Color(field="Nama Barang", type="nominal", legend=alt.Legend(title="Nama Perangkat", orient="right")),
                    tooltip=["Nama Barang", "Stok"]
                ).properties(height=265)
                
                st.altair_chart(pie_chart, use_container_width=True)
            else:
                st.info("Data barang kosong atau stok seluruhnya 0.")
            
    with st.container(border=True):
        st.markdown("""
            <div class="block-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z"/></svg>
                10 Transaksi Terakhir (Log Book)
            </div>
        """, unsafe_allow_html=True)
        if not df_log.empty:
            st.dataframe(df_log.sort_values(by="Waktu", ascending=False).head(10), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada riwayat aktivitas.")

# ==========================================
# 2. HALAMAN MANAJEMEN STOK (VERSI DIPERBAIKI)
# ==========================================
elif menu == "Manajemen Stok":
    st.markdown("""
        <div class="page-header-container">
            <h3 class="fw-bold text-dark m-0" style="font-size: 22px;">📦 Manajemen Stok Perangkat ISP</h3>
            <p class="text-muted small m-0" style="font-size: 13px; margin-top: 4px !important;">Cek volume dan ketersediaan barang real-time.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Masuk ke dalam container agar menyatu
    with st.container(border=True):
        st.markdown("<div class='block-header'>🔍 Pencarian & Tabel Stok Barang</div>", unsafe_allow_html=True)
        search_query = st.text_input("Cari Alat/Material:", placeholder="Ketik nama perangkat...")
        
        # Logika Filter
        if search_query:
            df_filtered = df_barang[df_barang["Nama Barang"].str.contains(search_query, case=False, na=False)]
        else:
            df_filtered = df_barang
            
        # PENTING: Gunakan st.dataframe agar ikon muncul otomatis
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
# ==========================================
# 3. HALAMAN BARANG MASUK
# ==========================================
elif menu == "Barang Masuk":
    st.markdown("""
        <div class="page-header-container">
            <h3 class="fw-bold text-dark m-0" style="font-size: 22px;">📥 Input Barang Masuk</h3>
            <p class="text-muted small m-0" style="font-size: 13px; margin-top: 4px !important;">Tambah stok barang dari supplier atau restock perangkat.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
            <div class="block-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v3h3a.5.5 0 0 0 0-1h-3z"/></svg>
                Form Input Barang Masuk
            </div>
        """, unsafe_allow_html=True)
        with st.form("form_masuk", clear_on_submit=True):
            pilih_item = st.selectbox("Pilih Perangkat:", df_barang["Nama Barang"].tolist() if not df_barang.empty else ["Data Kosong"])
            qty = st.number_input("Jumlah Masuk (Qty):", min_value=1, step=1)
            ket = st.text_input("Keterangan Tambahan / Supplier:")
            submit = st.form_submit_button("Simpan Data Masuk")
            
            if submit and not df_barang.empty:
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tgl_sekarang = datetime.now().strftime("%Y-%m-%d")
                
                df_masuk_baru = pd.DataFrame([{"Tanggal": tgl_sekarang, "Nama Barang": pilih_item, "Qty": qty, "Keterangan": ket}])
                df_masuk_baru.to_csv(FILE_MASUK, mode='a', header=False, index=False)
                
                df_barang.loc[df_barang["Nama Barang"] == pilih_item, "Stok"] += qty
                df_barang.to_csv(FILE_BARANG, index=False)
                
                pesan_log = f"Input Barang Masuk: {pilih_item} sebanyak {qty} unit. Ket: {ket}"
                pd.DataFrame([{"Waktu": waktu_sekarang, "Aktivitas": pesan_log}]).to_csv(FILE_LOG, mode='a', header=False, index=False)
                st.success(f"Berhasil menambahkan {qty} unit ke perangkat {pilih_item}!")

# ==========================================
# 4. HALAMAN BARANG KELUAR
# ==========================================
elif menu == "Barang Keluar":
    st.markdown("""
        <div class="page-header-container">
            <h3 class="fw-bold text-dark m-0" style="font-size: 22px;">📤 Input Barang Keluar</h3>
            <p class="text-muted small m-0" style="font-size: 13px; margin-top: 4px !important;">Catat pengeluaran barang untuk instalasi atau pemeliharaan lapangan.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
            <div class="block-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M4.5 7.5a.5.5 0 0 0 0 1h7a.5.5 0 0 0 0-1z"/></svg>
                Form Input Barang Keluar
            </div>
        """, unsafe_allow_html=True)
        with st.form("form_keluar", clear_on_submit=True):
            pilih_item = st.selectbox("Pilih Perangkat:", df_barang["Nama Barang"].tolist() if not df_barang.empty else ["Data Kosong"])
            qty = st.number_input("Jumlah Keluar (Qty):", min_value=1, step=1)
            teknisi_dipilih = st.selectbox("Nama Teknisi Pengambil:", df_teknisi["Nama Teknisi"].tolist() if not df_teknisi.empty else ["Data Teknisi Kosong"])
            keperluan = st.text_input("Lokasi Pemasangan / Project:")
            ket = st.text_input("Keterangan Tambahan:")
            submit = st.form_submit_button("Validasi Pengeluaran")
            
            if submit and not df_barang.empty:
                stok_ada = df_barang.loc[df_barang["Nama Barang"] == pilih_item, "Stok"].values[0]
                
                if stok_ada < qty:
                    st.error(f"❌ Transaksi Gagal! Stok {pilih_item} tidak cukup (Sisa di gudang: {stok_ada} pcs).")
                else:
                    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    tgl_sekarang = datetime.now().strftime("%Y-%m-%d")
                    
                    df_keluar_baru = pd.DataFrame([{"Tanggal": tgl_sekarang, "Nama Barang": pilih_item, "Teknisi": teknisi_dipilih, "Qty": qty, "Keperluan": keperluan, "Keterangan": ket}])
                    df_keluar_baru.to_csv(FILE_KELUAR, mode='a', header=False, index=False)
                    
                    df_barang.loc[df_barang["Nama Barang"] == pilih_item, "Stok"] -= qty
                    df_barang.to_csv(FILE_BARANG, index=False)
                    
                    pesan_log = f"Input Barang Keluar: {pilih_item} diambil oleh {teknisi_dipilih} sebanyak {qty} unit untuk {keperluan}."
                    pd.DataFrame([{"Waktu": waktu_sekarang, "Aktivitas": pesan_log}]).to_csv(FILE_LOG, mode='a', header=False, index=False)
                    st.success(f"✅ Pengeluaran {qty} unit {pilih_item} divalidasi dengan sukses!")
# ==========================================
# 5. HALAMAN LOG BOOK AKTIVITAS
# ==========================================
elif menu == "Log Book Aktivitas":
    st.markdown("""
        <div class="page-header-container">
            <h3 class="fw-bold text-dark m-0" style="font-size: 22px;">📜 Log Book Seluruh Aktivitas</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<div class='block-header'>History Log Book</div>", unsafe_allow_html=True)
        
        # Membuat Tabs untuk filter
        tab_semua, tab_masuk, tab_keluar = st.tabs(["🕒 Semua Riwayat", "📥 Barang Masuk", "📤 Barang Keluar"])
        
        with tab_semua:
            st.dataframe(df_log.sort_values(by="Waktu", ascending=False), use_container_width=True, hide_index=True)
            
        with tab_masuk:
            df_masuk_log = df_log[df_log["Aktivitas"].str.contains("Masuk", case=False, na=False)]
            st.dataframe(df_masuk_log.sort_values(by="Waktu", ascending=False), use_container_width=True, hide_index=True)
            
        with tab_keluar:
            df_keluar_log = df_log[df_log["Aktivitas"].str.contains("Keluar", case=False, na=False)]
            st.dataframe(df_keluar_log.sort_values(by="Waktu", ascending=False), use_container_width=True, hide_index=True)
