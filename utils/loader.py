import pickle
import streamlit as st

@st.cache_resource
def load_model():
    from tensorflow.keras.models import load_model
    return load_model("model/best_hdfs_lstm.keras")

@st.cache_resource
def load_vocab():
    with open("model/event_to_idx.pkl", "rb") as f:
        return pickle.load(f)