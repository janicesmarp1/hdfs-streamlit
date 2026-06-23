import streamlit as st
from utils.loader import load_model, load_vocab
from utils.preprocess import parse_seq
from utils.predictor import run_prediction

st.set_page_config(
    page_title="Deteksi Anomali HDFS",
    page_icon="🔍",
    layout="centered"
)

model = load_model()
vocab = load_vocab()

st.markdown("""
<style>

/* ===== FONT ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ===== BACKGROUND ===== */
.stApp{
    background:
    radial-gradient(circle at top left,#60A5FA22 0%,transparent 35%),
    radial-gradient(circle at bottom right,#2563EB22 0%,transparent 35%),
    linear-gradient(135deg,#F8FBFF 0%,#EFF6FF 40%,#DBEAFE 100%);
}

/* ===== CONTENT WIDTH ===== */
.main .block-container{
    max-width:1000px;
    padding-top:2rem;
    padding-bottom:3rem;
}

/* ===== HEADER CARD ===== */
.hero{
    background:rgba(255,255,255,0.65);
    backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,0.6);
    border-radius:24px;
    padding:28px;
    text-align:center;
    box-shadow:0 10px 35px rgba(37,99,235,0.08);
    margin-bottom:25px;
}

.hero-title{
    font-size:2rem;
    font-weight:700;
    color:#0F172A;
    margin-bottom:5px;
}

.hero-sub{
    color:#64748B;
    font-size:0.95rem;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"]{
    background:rgba(255,255,255,0.75);
    backdrop-filter:blur(12px);
    border-radius:18px;
    border:1px solid #DCEAFE;
    padding:12px;
}

/* ===== BUTTON ===== */
.stButton > button{
    width:100%;
    border:none;
    border-radius:16px;
    padding:14px;
    font-weight:600;
    font-size:15px;

    background:linear-gradient(
        135deg,
        #2563EB,
        #3B82F6
    );

    color:white;

    box-shadow:
        0 8px 25px rgba(37,99,235,0.25);

    transition:all .25s ease;
}

.stButton > button:hover{
    transform:translateY(-2px);
    box-shadow:
        0 12px 30px rgba(37,99,235,0.35);
}

/* ===== METRIC CARDS ===== */
.metric-card{
    background:rgba(255,255,255,0.8);
    backdrop-filter:blur(12px);

    border:1px solid rgba(255,255,255,0.6);

    border-radius:18px;

    padding:18px;

    text-align:center;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.04);
}

.metric-title{
    font-size:12px;
    text-transform:uppercase;
    color:#64748B;
    letter-spacing:1px;
}

.metric-value{
    font-size:30px;
    font-weight:700;
    color:#2563EB;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"]{
    border-radius:18px;
    overflow:hidden;
    border:1px solid #DBEAFE;
}

/* ===== TABS ===== */
.stTabs [role="tablist"]{
    gap:8px;
}

.stTabs [role="tab"]{
    border-radius:12px;
    padding:10px 18px;
}

.stTabs [aria-selected="true"]{
    background:#2563EB !important;
    color:white !important;
}

/* ===== SLIDER ===== */
[data-baseweb="slider"] [role="slider"]{
    background:#2563EB !important;
    border-color:#2563EB !important;
}

/* ===== FOOTER ===== */
.footer{
    text-align:center;
    color:#94A3B8;
    font-size:13px;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div style="font-size:48px;">🔍</div>

    <div class="hero-title">
        HDFS Anomaly Detection
    </div>

    <div class="hero-sub">
        Bidirectional LSTM-Based Log Anomaly Detection System
    </div>
</div>
""", unsafe_allow_html=True)

threshold = st.slider(
    "Threshold",
    min_value=0.01,
    max_value=0.99,
    value=0.50
)

trace_file = st.file_uploader(
    "Upload Event Trace CSV",
    type=["csv"]
)

label_file = st.file_uploader(
    "Upload Anomaly Label CSV (Opsional)",
    type=["csv"]
)

if st.button("Deteksi") and trace_file:

    result_df = run_prediction(
        trace_file,
        model,
        vocab,
        threshold
    )

    st.success("Deteksi selesai")
    total = len(result_df)
anomali = len(result_df[result_df["status"] == "🚨 Anomali"])
normal = total - anomali

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL</div>
        <div class="metric-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">NORMAL</div>
        <div class="metric-value">{normal}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">ANOMALI</div>
        <div class="metric-value">{anomali}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">THRESHOLD</div>
        <div class="metric-value">{threshold:.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(result_df)

    st.download_button(
        "Download Hasil",
        result_df.to_csv(index=False),
        file_name="hasil_deteksi.csv"
    )
    