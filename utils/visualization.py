import matplotlib.pyplot as plt
import streamlit as st

def plot_distribution(normal, anomaly):

    fig, ax = plt.subplots()

    ax.pie(
        [normal, anomaly],
        labels=["Normal", "Anomali"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)