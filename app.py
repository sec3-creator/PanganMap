%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pickle

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
    .cluster-box {
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #00b894;
        background: rgba(255,255,255,0.03);
    }
    .cluster-box h4 {
        margin: 0;
        color: #00b894;
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
st.markdown('<div class="sub-title">📍 Peta Interaktif Harga Pangan & Clustering Provinsi</div>', unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
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
except FileNotFoundError as e:
    st.error(f"❌ File tidak ditemukan: {e}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error: {e}")
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
    
    # Info clustering
    if selected in cluster_results:
        result = cluster_results[selected]
        st.markdown(f"**🔢 Cluster**: {result['n_clusters']}")
        st.markdown(f"**📊 Silhouette**: {result['silhouette_score']:.4f}")
    
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

# ============ PETA DENGAN CLUSTER ============
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

# Warna untuk cluster
cluster_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

fig = px.scatter_geo(
    geo_data,
    lat='lat',
    lon='lon',
    hover_name='Provinsi',
    color='Cluster',
    size='Harga',
    size_max=40,
    color_continuous_scale='Viridis',
    title=f'Clustering Harga {selected} - {result["n_clusters"]} Cluster',
    template='plotly_dark'
)

fig.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>' +
                  '💰 Harga: Rp %{marker.size:,.0f}<br>' +
                  '🔢 Cluster: %{marker.color}<br>' +
                  '📊 Kategori: %{customdata[0]}<br>' +
                  '📈 Volatilitas: %{customdata[1]}<br>' +
                  '<extra></extra>',
    customdata=geo_data[['Kategori', 'Volatilitas']].values,
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
        title="Cluster",
        len=0.5,
        thickness=20
    )
)

st.plotly_chart(fig, use_container_width=True)

# INTERPRETASI CLUSTER
st.subheader("📝 Cluster")

cols = st.columns(len(interpretation))
for idx, (cluster_id, info) in enumerate(interpretation.items()):
    with cols[idx % len(cols)]:
        color = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'][idx % 5]
        st.markdown(f"""
        <div class="cluster-box" style="border-left-color: {color};">
            <h4>Cluster {cluster_id}</h4>
            <p><b>Deskripsi:</b> {info['deskripsi']}</p>
            <p><b>Provinsi:</b> {info['jumlah']}</p>
            <p><b>Rata-rata:</b> Rp {info['rata_rata']:,.0f}</p>
            <p><b>Provinsi:</b> {', '.join(info['provinsi'][:4])}{' ...' if len(info['provinsi']) > 4 else ''}</p>
        </div>
        """, unsafe_allow_html=True)

# TABEL
st.subheader("📋 Data Lengkap Per Provinsi")
table_data = geo_data[['Provinsi', 'Cluster', 'Kategori', 'Volatilitas', 'Harga']].copy()
table_data['Harga'] = table_data['Harga'].map(lambda x: f"Rp {x:,.0f}")
table_data = table_data.sort_values('Provinsi')
st.dataframe(table_data, use_container_width=True, height=400)

# DOWNLOAD
csv = geo_data.to_csv(index=False)
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f'panganmap_cluster_{selected}.csv',
    mime='text/csv'
)

# FOOTER
st.markdown('<div class="footer">🗺️ PanganMap • Clustering Harga Pangan Indonesia</div>', unsafe_allow_html=True)
