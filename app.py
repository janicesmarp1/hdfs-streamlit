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

.stApp{
    background: linear-gradient(
        160deg,
        #DBEAFE 0%,
        #EFF6FF 45%,
        #FFFFFF 100%
    );
}

.main .block-container{
    max-width:900px;
    padding-top:2rem;
}

h1{
    color:#1565C0;
    text-align:center;
}

.stButton > button{
    width:100%;
    background:#1565C0;
    color:white;
    border:none;
    border-radius:12px;
    padding:0.7rem;
    font-weight:bold;
}

.stButton > button:hover{
    background:#0D47A1;
}

[data-testid="stFileUploader"]{
    background:white;
    border-radius:12px;
    padding:10px;
    border:1px solid #BFDBFE;
}

.metric-card{
    background:white;
    padding:15px;
    border-radius:12px;
    border:1px solid #DBEAFE;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
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
    st.dataframe(result_df)

    st.download_button(
        "Download Hasil",
        result_df.to_csv(index=False),
        file_name="hasil_deteksi.csv"
    )