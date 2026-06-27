import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="PanganMap - Peta Harga Pangan Indonesia",
    page_icon="🗺️",
    layout="wide"
)

# CSS BRANDING
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00b894, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-title {
        text-align: center;
        color: #b2bec3;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00b894;
    }
    .metric-label {
        color: #b2bec3;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        color: #636e72;
        padding: 2rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-title">🗺️ PanganMap</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">📍 Peta Interaktif Harga Pangan Seluruh Indonesia</div>', unsafe_allow_html=True)

# LOAD DATA REAL
@st.cache_data
def load_data():
    """Load data real dari file Excel"""
    df = pd.read_excel('Harga Pangan.xlsx')
    return df

# KOORDINAT PROVINSI
COORDS = {
    'Aceh': [4.5, 96.5], 'Bali': [-8.3, 115.2], 'Banten': [-6.1, 106.1],
    'Bengkulu': [-3.8, 102.3], 'DI Yogyakarta': [-7.8, 110.4], 'Gorontalo': [0.5, 123.1],
    'Jambi': [-1.6, 103.6], 'Jawa Barat': [-6.9, 107.6], 'Jawa Tengah': [-7.2, 110.0],
    'Jawa Timur': [-7.5, 112.7], 'Kalimantan Barat': [-0.1, 110.5],
    'Kalimantan Selatan': [-3.3, 114.6], 'Kalimantan Tengah': [-1.7, 113.0],
    'Kalimantan Timur': [0.5, 116.0], 'Kalimantan Utara': [2.0, 116.0],
    'Kepulauan Bangka Belitung': [-2.5, 106.5], 'Kepulauan Riau': [0.9, 104.5],
    'Lampung': [-5.4, 105.3], 'Maluku': [-3.2, 130.0], 'Maluku Utara': [1.0, 128.0],
    'Nusa Tenggara Barat': [-8.6, 116.5], 'Papua': [-4.0, 138.0], 'Papua Barat': [-1.0, 133.0],
    'Riau': [0.5, 101.5], 'Sulawesi Barat': [-2.7, 119.0], 'Sulawesi Selatan': [-4.0, 120.0],
    'Sulawesi Tengah': [-1.0, 121.0], 'Sulawesi Tenggara': [-4.0, 122.0],
    'Sulawesi Utara': [1.0, 124.5], 'Sumatera Barat': [-1.0, 100.5],
    'Sumatera Selatan': [-3.0, 104.0], 'Sumatera Utara': [2.0, 99.0]
}

# MAIN
try:
    df = load_data()
    st.success("Data real berhasil dimuat dari Harga Pangan.xlsx")
except FileNotFoundError:
    st.error("File 'Harga Pangan.xlsx' tidak ditemukan! Upload file Excel ke repository.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    
    if 'Komoditas' in df.columns:
        komoditas_list = df['Komoditas'].unique().tolist()
        selected = st.selectbox("📌 Pilih Komoditas", komoditas_list)
        df_filter = df[df['Komoditas'] == selected]
    else:
        df_filter = df
    
    st.markdown("---")
    st.markdown(f"**📍 Provinsi**: {df_filter['Provinsi'].nunique()}")
    if 'Tanggal' in df_filter.columns:
        st.markdown(f"**📅 Periode**: {df_filter['Tanggal'].min().strftime('%d %b %Y')} - {df_filter['Tanggal'].max().strftime('%d %b %Y')}")
    st.markdown("---")
    st.caption("Made with ❤️ | PanganMap")

# METRICS
avg = df_filter['Harga'].mean()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {avg:,.0f}</div>
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

# PETA
st.markdown("### 🗺️ Peta Sebaran Harga")

geo_data = df_filter.groupby('Provinsi')['Harga'].mean().reset_index()
geo_data['lat'] = geo_data['Provinsi'].map(lambda x: COORDS.get(x, [0,0])[0])
geo_data['lon'] = geo_data['Provinsi'].map(lambda x: COORDS.get(x, [0,0])[1])

fig = px.scatter_geo(
    geo_data,
    lat='lat',
    lon='lon',
    hover_name='Provinsi',
    color='Harga',
    size='Harga',
    size_max=35,
    color_continuous_scale=[
        (0, '#2ecc71'),
        (0.3, '#27ae60'),
        (0.5, '#f1c40f'),
        (0.7, '#e67e22'),
        (1.0, '#e74c3c')
    ],
    template='plotly_dark',
    title=f'Sebaran Harga {selected if "Komoditas" in df.columns else "Pangan"}'
)

fig.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>💰 Harga: Rp %{marker.size:,.0f}<br><extra></extra>',
    marker=dict(line=dict(width=2, color='white'), opacity=0.9)
)

fig.update_layout(
    height=600,
    geo=dict(
        showland=True,
        landcolor='#1a472a',
        showocean=True,
        oceancolor='#0a1628',
        showcountries=True,
        countrycolor='#2d6a4f',
        coastlinecolor='#2d6a4f',
        showframe=False
    ),
    coloraxis_colorbar=dict(
        title="Harga (Rp)",
        tickprefix="Rp ",
        len=0.5,
        thickness=20
    )
)

st.plotly_chart(fig, use_container_width=True)

# TABEL
st.subheader("📋 Data Lengkap Per Provinsi")
table_data = geo_data[['Provinsi', 'Harga']].copy()
table_data['Harga'] = table_data['Harga'].map(lambda x: f"Rp {x:,.0f}")
table_data = table_data.sort_values('Provinsi')
st.dataframe(table_data, use_container_width=True, height=400)

# DOWNLOAD
csv = geo_data.to_csv(index=False)
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f'panganmap_{selected if "Komoditas" in df.columns else "data"}.csv',
    mime='text/csv'
)

# FOOTER
st.markdown('<div class="footer">🗺️ PanganMap • Peta Interaktif Harga Pangan Indonesia</div>', unsafe_allow_html=True)

from google.colab import files
files.download('app.py')
