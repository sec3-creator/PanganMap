import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="🌍 PanganMap",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d2ff, #3a7bd5, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(0, 210, 255, 0.2); }
        to { text-shadow: 0 0 60px rgba(0, 210, 255, 0.6); }
    }
    
    .sub-title {
        text-align: center;
        color: #8892b0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.2rem;
        text-align: center;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 210, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #8892b0;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #00d2ff, #3a7bd5) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        transition: transform 0.3s !important;
    }
    
    .stDownloadButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 30px rgba(0, 210, 255, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('Harga Pangan.xlsx')
        return df
    except:
        return None

@st.cache_data
def generate_data():
    provinsi = [
        'Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi', 
        'Sumatera Selatan', 'Bengkulu', 'Lampung', 'Kepulauan Bangka Belitung',
        'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 
        'DI Yogyakarta', 'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat',
        'Nusa Tenggara Timur', 'Kalimantan Barat', 'Kalimantan Tengah',
        'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara',
        'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan',
        'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat', 'Maluku',
        'Maluku Utara', 'Papua', 'Papua Barat'
    ]
    
    coords = {
        'Aceh': [4.5, 96.5], 'Sumatera Utara': [2.0, 99.0], 'Sumatera Barat': [-1.0, 100.5],
        'Riau': [0.5, 101.5], 'Jambi': [-1.6, 103.6], 'Sumatera Selatan': [-3.0, 104.0],
        'Bengkulu': [-3.8, 102.3], 'Lampung': [-5.4, 105.3], 
        'Kepulauan Bangka Belitung': [-2.5, 106.5], 'Kepulauan Riau': [0.9, 104.5],
        'DKI Jakarta': [-6.2, 106.8], 'Jawa Barat': [-6.9, 107.6], 'Jawa Tengah': [-7.2, 110.0],
        'DI Yogyakarta': [-7.8, 110.4], 'Jawa Timur': [-7.5, 112.7], 'Banten': [-6.1, 106.1],
        'Bali': [-8.3, 115.2], 'Nusa Tenggara Barat': [-8.6, 116.5], 'Nusa Tenggara Timur': [-8.6, 120.0],
        'Kalimantan Barat': [-0.1, 110.5], 'Kalimantan Tengah': [-1.7, 113.0],
        'Kalimantan Selatan': [-3.3, 114.6], 'Kalimantan Timur': [0.5, 116.0],
        'Kalimantan Utara': [2.0, 116.0], 'Sulawesi Utara': [1.0, 124.5],
        'Sulawesi Tengah': [-1.0, 121.0], 'Sulawesi Selatan': [-4.0, 120.0],
        'Sulawesi Tenggara': [-4.0, 122.0], 'Gorontalo': [0.5, 123.1],
        'Sulawesi Barat': [-2.7, 119.0], 'Maluku': [-3.2, 130.0],
        'Maluku Utara': [1.0, 128.0], 'Papua': [-4.0, 138.0], 'Papua Barat': [-1.0, 133.0]
    }
    
    komoditas = ['Cabai Merah', 'Daging Ayam', 'Telur Ayam']
    dates = pd.date_range('2025-01-01', '2026-05-27', freq='W')
    
    data = []
    for prov in provinsi:
        for kom in komoditas:
            base = np.random.uniform(15000, 50000)
            trend = np.linspace(0, np.random.uniform(-0.2, 0.3), len(dates))
            noise = np.random.normal(0, 3000, len(dates))
            prices = base * (1 + trend) + noise
            prices = np.maximum(prices, 5000)
            
            for date, price in zip(dates, prices):
                data.append({
                    'Provinsi': prov,
                    'Tanggal': date,
                    'Komoditas': kom,
                    'Harga': round(price, 2),
                    'lat': coords.get(prov, [0,0])[0],
                    'lon': coords.get(prov, [0,0])[1]
                })
    
    return pd.DataFrame(data)

# MAIN
df = generate_data()
df_real = load_data()
if df_real is not None:
    df = df_real

komoditas_list = df['Komoditas'].unique().tolist() if 'Komoditas' in df.columns else ['Harga']

# SIDEBAR
with st.sidebar:
    st.markdown("## 🗺️ Peta")
    st.markdown("---")
    
    selected = st.selectbox("📌 Pilih Komoditas", komoditas_list)
    
    if 'Komoditas' in df.columns:
        min_price = int(df[df['Komoditas'] == selected]['Harga'].min())
        max_price = int(df[df['Komoditas'] == selected]['Harga'].max())
    else:
        min_price = int(df['Harga'].min())
        max_price = int(df['Harga'].max())
    
    price_range = st.slider(
        "💰 Rentang Harga",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )
    
    st.markdown("---")
    st.markdown("### 🎨 Legenda")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
        <div style="display: flex; align-items: center; gap: 10px; margin: 5px 0;">
            <div style="width: 20px; height: 20px; border-radius: 50%; background: #00d2ff; box-shadow: 0 0 20px #00d2ff;"></div>
            <span style="color: #8892b0;">Harga Tinggi</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; margin: 5px 0;">
            <div style="width: 20px; height: 20px; border-radius: 50%; background: #7bed9f; box-shadow: 0 0 20px #7bed9f;"></div>
            <span style="color: #8892b0;">Harga Sedang</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; margin: 5px 0;">
            <div style="width: 20px; height: 20px; border-radius: 50%; background: #ff6b6b; box-shadow: 0 0 20px #ff6b6b;"></div>
            <span style="color: #8892b0;">Harga Rendah</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-title">🌍 Peta Harga Pangan Nusantara</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">✨ Analisis {selected} di 34 Provinsi</div>', unsafe_allow_html=True)

# FILTER DATA
if 'Komoditas' in df.columns:
    df_filter = df[df['Komoditas'] == selected]
else:
    df_filter = df

df_filter = df_filter[(df_filter['Harga'] >= price_range[0]) & (df_filter['Harga'] <= price_range[1])]

# METRICS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {df_filter['Harga'].mean():,.0f}</div>
        <div class="metric-label">📊 Rata-rata Harga</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {df_filter['Harga'].max():,.0f}</div>
        <div class="metric-label">⬆️ Harga Tertinggi</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {df_filter['Harga'].min():,.0f}</div>
        <div class="metric-label">⬇️ Harga Terendah</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df_filter['Provinsi'].nunique()}</div>
        <div class="metric-label">📍 Provinsi</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# PETA KEREN
st.markdown("### 🗺️ Peta")

geo_data = df_filter.groupby('Provinsi').agg({
    'Harga': 'mean',
    'lat': 'first',
    'lon': 'first'
}).reset_index()

# PETA
fig = px.scatter_geo(
    geo_data,
    lat='lat',
    lon='lon',
    hover_name='Provinsi',
    color='Harga',
    size='Harga',
    size_max=40,
    color_continuous_scale=[
        (0, '#2ecc71'),    # Hijau terang
        (0.3, '#27ae60'),  # Hijau
        (0.5, '#f1c40f'),  # Kuning
        (0.7, '#e67e22'),  # Orange
        (1.0, '#e74c3c')   # Merah
    ],
    title=f'<b>{selected}</b> - Sebaran Harga per Provinsi',
    template='plotly_dark'
)

fig.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>' +
                  '💰 Harga: Rp %{marker.size:,.0f}<br>' +
                  '<extra></extra>',
    marker=dict(line=dict(width=2, color='white'), opacity=0.9)
)

fig.update_layout(
    geo=dict(
        showland=True,
        landcolor='#1a472a',  # HIJAU HUTAN GELAP
        lakecolor='#0a3d62',
        oceancolor='#0a1628',
        showocean=True,
        showcountries=True,
        countrycolor='#2d6a4f',
        coastlinecolor='#2d6a4f',
        showframe=False,
        projection_type='natural earth',
        lataxis=dict(range=[-12, 8]),
        lonaxis=dict(range=[95, 142])
    ),
    height=650,
    margin=dict(l=0, r=0, t=50, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#8892b0'),
    coloraxis_colorbar=dict(
        title="Harga (Rp)",
        tickprefix="Rp ",
        len=0.5,
        thickness=20,
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='rgba(255,255,255,0.1)',
        borderwidth=1
    )
)

st.plotly_chart(fig, use_container_width=True)

# TABEL DATA
st.markdown("---")
st.markdown("### 📋 Data Lengkap Per Provinsi")

table_data = geo_data[['Provinsi', 'Harga']].copy()
table_data['Harga'] = table_data['Harga'].map(lambda x: f"Rp {x:,.0f}")
table_data = table_data.sort_values('Provinsi')

st.dataframe(table_data, use_container_width=True, height=400)

# Download
csv = geo_data.to_csv(index=False)
st.download_button(
    label="📥 Download Data CSV",
    data=csv,
    file_name=f'data_harga_{selected.replace(" ", "_")}.csv',
    mime='text/csv'
)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8892b0; padding: 2rem 0;">
    🌏 Dibuat dengan ❤️ • Data Harga Pangan Indonesia
</div>
""", unsafe_allow_html=True)
