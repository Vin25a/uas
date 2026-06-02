# app.py

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import time

from graph_logic import create_graph, shortest_path
from data import wisata

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="DSS Wisata Bali",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    color: white;
}

/* HIDE STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* TITLE */
.main-title {
    text-align: center;
    font-size: 65px;
    font-weight: 800;
    background: linear-gradient(90deg,#38bdf8,#0ea5e9,#22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glow 2s infinite alternate;
    margin-top: 20px;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #38bdf8;
    }
    to {
        text-shadow: 0 0 25px #0ea5e9;
    }
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 40px;
}

/* CARD */
.card {
    background: rgba(30,41,59,0.75);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 25px;
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    transition: 0.4s;
    animation: fadeInUp 0.7s ease;
}

.card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 12px 35px rgba(56,189,248,0.3);
}

/* BUTTON */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#06b6d4,#0ea5e9);
    color: white;
    border: none;
    border-radius: 15px;
    padding: 14px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px #0ea5e9;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] {
    background-color: #0f172a;
    border-radius: 12px;
}

/* METRIC */
.metric {
    font-size: 24px;
    font-weight: bold;
    color: #38bdf8;
    margin-top: 10px;
}

/* ANIMATION */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #0ea5e9;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GRAPH
# =========================
G = create_graph()

# =========================
# HEADER
# =========================
st.markdown("""
<div class='main-title'>
🌴 BALI SMART TOURISM
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Sistem Pendukung Keputusan Wisata Bali Berbasis Graph & Shortest Path
</div>
""", unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
left, right = st.columns([1, 2])

# =========================
# LEFT PANEL
# =========================
with left:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📍 Pilih Lokasi")

    nodes = list(G.nodes())

    start = st.selectbox(
        "Lokasi Awal",
        nodes
    )

    end = st.selectbox(
        "Tujuan Wisata",
        nodes
    )

    cari = st.button("🚀 Cari Jalur Terbaik")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# RIGHT PANEL
# =========================
with right:

    if cari:

        with st.spinner("🔍 Sedang mencari rute terbaik..."):
            time.sleep(2)

        try:

            path, distance = shortest_path(G, start, end)

            st.markdown("<div class='card'>", unsafe_allow_html=True)

            toast = st.toast(
                '🎉 Rute berhasil ditemukan!',
                icon='✅'
            )

            st.markdown(
                "<div class='metric'>🛣️ Jalur Wisata</div>",
                unsafe_allow_html=True
            )

            st.write(" ➜ ".join(path))

            st.markdown(
                f"<div class='metric'>📏 Total Jarak : {distance} KM</div>",
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

            # =========================
            # VISUALISASI GRAPH
            # =========================
            fig, ax = plt.subplots(figsize=(12, 8))

            fig.patch.set_facecolor('#020617')
            ax.set_facecolor('#020617')

            pos = nx.spring_layout(G, seed=7)

            # node
            nx.draw_networkx_nodes(
                G,
                pos,
                node_color="#06b6d4",
                node_size=3200
            )

            # edge
            nx.draw_networkx_edges(
                G,
                pos,
                edge_color="white",
                width=2
            )

            # label
            nx.draw_networkx_labels(
                G,
                pos,
                font_size=10,
                font_color="white",
                font_weight="bold"
            )

            # edge label
            edge_labels = nx.get_edge_attributes(G, 'weight')

            nx.draw_networkx_edge_labels(
                G,
                pos,
                edge_labels=edge_labels,
                font_color='yellow'
            )

            # highlight path
            path_edges = list(zip(path, path[1:]))

            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=path_edges,
                edge_color="#ef4444",
                width=6
            )

            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.subheader("🗺️ Visualisasi Jalur")

            st.pyplot(fig)

            st.markdown("</div>", unsafe_allow_html=True)

        except:
            st.error("❌ Jalur tidak ditemukan")

# =========================
# DATA WISATA
# =========================
st.write("")
st.write("")

st.markdown("""
<h2 style='text-align:center;color:#38bdf8;'>
📋 Destinasi Wisata Bali
</h2>
""", unsafe_allow_html=True)

cols = st.columns(3)

i = 0

for asal in wisata:

    with cols[i % 3]:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown(f"### 📍 {asal}")

        for tujuan, jarak in wisata[asal].items():
            st.write(f"➡️ {tujuan} — {jarak} KM")

        st.markdown("</div>", unsafe_allow_html=True)

    i += 1