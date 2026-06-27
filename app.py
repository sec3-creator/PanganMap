import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="PanganMap - Peta Harga Pangan Indonesia",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS SUPER KEREN
st.markdown("""
<style>
    /* Background gradien gelap*/
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
        transition: transform 0.3s, box-shadow 0.3s;
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
    
    /* CLUSTER BOX - TULISAN PUTIH TERANG */
    .cluster-box {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #00d2ff;
        transition: transform 0.3s;
    }
    
    .cluster-box:hover {
        transform: scale(1.02);
    }
    
    .cluster-box h4 {
        margin: 0;
        color: #ffffff !important;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .cluster-box p {
        color: #e0e0e0 !important;
        margin: 0.3rem 0;
        font-size: 0.95rem;
    }
    
    .cluster-box b {
        color: #ffffff !important;
    }
    
    .footer {
        text-align: center;
        color: #636e72;
        padding: 2rem 0;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(10px);
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

# HEADER
st.markdown('<div class="main-title">🗺️ PanganMap</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">📍 Analisis Clustering Harga Pangan 32 Provinsi Indonesia</div>', unsafe_allow_html=True)

# LOAD DATA
def load_data():
    df = pd.read_excel('Harga Pangan.xlsx')
    return df

@st.cache_data
def load_cluster_results():
    with open('cluster_results.pkl', 'rb') as f:
        cluster_results = pickle.load(f)
    with open('cluster_analysis.pkl', 'rb') as f:
        cluster_analysis = pickle.load(f)
    return cluster_results, cluster_analysis

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
    cluster_results, cluster_analysis = load_cluster_results()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    
    komoditas_list = df['Komoditas'].unique().tolist()
    selected = st.selectbox("📌 Pilih Komoditas", komoditas_list)
    
    df_filter = df[df['Komoditas'] == selected]
    
    st.markdown("---")
    st.markdown(f"**📍 Provinsi**: {df_filter['Provinsi'].nunique()}")
    st.markdown(f"**📅 Periode**: {df_filter['Tanggal'].min().strftime('%d %b %Y')} - {df_filter['Tanggal'].max().strftime('%d %b %Y')}")
    
    if selected in cluster_results:
        result = cluster_results[selected]
        st.markdown(f"**🔢 Cluster**: {result['n_clusters']}")
        st.markdown(f"**📊 Silhouette**: {result['silhouette_score']:.4f}")
    
    st.markdown("---")
    st.caption("Made with ❤️ | PanganMap")

# METRICS
avg = df_filter['Harga'].mean()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {avg:,.0f}</div>
        <div class="metric-label">📊 Rata-rata</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {df_filter['Harga'].max():,.0f}</div>
        <div class="metric-label">⬆️ Tertinggi</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {df_filter['Harga'].min():,.0f}</div>
        <div class="metric-label">⬇️ Terendah</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    result = cluster_results[selected]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{result['n_clusters']}</div>
        <div class="metric-label">🔢 Cluster</div>
    </div>
    """, unsafe_allow_html=True)

# PETA CLUSTER - 32 PROVINSI
st.markdown("### 🗺️ Peta Clustering Provinsi")

# Ambil data cluster
result = cluster_results[selected]
labels = result['labels']
provinsi_list = result['provinsi_list']
provinsi_cluster = dict(zip(provinsi_list, labels + 1))

# Siapkan data geo
geo_data = df_filter.groupby('Provinsi')['Harga'].mean().reset_index()
geo_data['Cluster'] = geo_data['Provinsi'].map(provinsi_cluster)

# Tambahkan interpretasi
interpretation = cluster_analysis[selected]['interpretation']
geo_data['Kategori'] = geo_data['Cluster'].map(
    lambda x: interpretation[x]['kategori_harga'] if x in interpretation else '-'
)
geo_data['Volatilitas'] = geo_data['Cluster'].map(
    lambda x: interpretation[x]['volatilitas'] if x in interpretation else '-'
)
geo_data['Deskripsi'] = geo_data['Cluster'].map(
    lambda x: interpretation[x]['deskripsi'] if x in interpretation else '-'
)

geo_data['lat'] = geo_data['Provinsi'].map(lambda x: COORDS.get(x, [0,0])[0])
geo_data['lon'] = geo_data['Provinsi'].map(lambda x: COORDS.get(x, [0,0])[1])

# Buat peta dengan warna cluster - 32 PROVINSI
fig = px.scatter_geo(
    geo_data,
    lat='lat',
    lon='lon',
    hover_name='Provinsi',
    color='Cluster',
    size='Harga',
    size_max=45,
    color_continuous_scale='Viridis',
    title=f'<b>{selected}</b> - Clustering 32 Provinsi',
    template='plotly_dark'
)

fig.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>' +
                  '💰 Harga: Rp %{marker.size:,.0f}<br>' +
                  '🔢 Cluster: %{marker.color}<br>' +
                  '📊 Kategori: %{customdata[0]}<br>' +
                  '📈 Volatilitas: %{customdata[1]}<br>' +
                  '📝 Deskripsi: %{customdata[2]}<br>' +
                  '<extra></extra>',
    customdata=geo_data[['Kategori', 'Volatilitas', 'Deskripsi']].values,
    marker=dict(line=dict(width=2, color='white'), opacity=0.9)
)

fig.update_layout(
    height=650,
    geo=dict(
        showland=True,
        landcolor='#1a472a',
        showocean=True,
        oceancolor='#0a1628',
        showcountries=True,
        countrycolor='#2d6a4f',
        coastlinecolor='#2d6a4f',
        showframe=False,
        lataxis=dict(range=[-12, 8]),
        lonaxis=dict(range=[95, 142])
    ),
    coloraxis_colorbar=dict(
        title="Cluster",
        len=0.5,
        thickness=20,
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='rgba(255,255,255,0.1)',
        borderwidth=1
    )
)

st.plotly_chart(fig, use_container_width=True)

# CLUSTER
st.subheader("📝 Cluster")

cols = st.columns(len(interpretation))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

for idx, (cluster_id, info) in enumerate(interpretation.items()):
    with cols[idx % len(cols)]:
        color = colors[idx % len(colors)]
        st.markdown(f"""
        <div class="cluster-box" style="border-left-color: {color};">
            <h4 style="color: {color};">Cluster {cluster_id}</h4>
            <p><b>Deskripsi:</b> {info['deskripsi']}</p>
            <p><b>Provinsi:</b> {info['jumlah']}</p>
            <p><b>Rata-rata:</b> Rp {info['rata_rata']:,.0f}</p>
            <p><b>Provinsi:</b> {', '.join(info['provinsi'][:4])}{' ...' if len(info['provinsi']) > 4 else ''}</p>
        </div>
        """, unsafe_allow_html=True)

# TABEL
st.subheader("📋 Data Lengkap Per Provinsi")
table_data = geo_data[['Provinsi', 'Cluster', 'Kategori', 'Volatilitas', 'Deskripsi', 'Harga']].copy()
table_data['Harga'] = table_data['Harga'].map(lambda x: f"Rp {x:,.0f}")
table_data = table_data.sort_values('Provinsi')

st.dataframe(
    table_data,
    use_container_width=True,
    height=450,
    column_config={
        "Provinsi": "📍 Provinsi",
        "Cluster": "🔢 Cluster",
        "Kategori": "📊 Kategori",
        "Volatilitas": "📈 Volatilitas",
        "Deskripsi": "📝 Deskripsi",
        "Harga": "💰 Harga"
    }
)

# DOWNLOAD
csv = geo_data.to_csv(index=False)
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f'panganmap_cluster_{selected}.csv',
    mime='text/csv'
)

# FOOTER
st.markdown('<div class="footer">🗺️ PanganMap • Analisis Clustering Harga Pangan Indonesia</div>', unsafe_allow_html=True)
