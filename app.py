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

st.title("🔍 Deteksi Anomali HDFS")

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