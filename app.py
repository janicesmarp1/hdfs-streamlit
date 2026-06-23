import streamlit as st
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Deteksi Anomali HDFS", page_icon="🔍", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: linear-gradient(160deg, #DBEAFE 0%, #EFF6FF 45%, #FFFFFF 100%);
    min-height: 100vh;
}

[data-testid="collapsedControl"] { display: none; }

.main .block-container {
    max-width: 500px;
    padding: 3.5rem 2rem 5rem 2rem;
    margin: 0 auto;
}

/* ── header ── */
.hdr-icon  { text-align:center; font-size:2rem; margin-bottom:0.4rem; }
.hdr-title { text-align:center; color:#1565C0; font-size:1.45rem; font-weight:700; margin:0 0 0.2rem 0; }
.hdr-sub   { text-align:center; color:#93C5FD; font-size:0.83rem; margin:0 0 2.2rem 0; }

/* ── section label ── */
.sec-lbl {
    color:#1565C0; font-size:0.63rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px; margin-bottom:0.5rem;
}
.sec-hint { color:#93C5FD; font-size:0.75rem; margin-top:0.3rem; }
.sec-gap  { margin-bottom:1.2rem; }

/* ── hide streamlit labels ── */
[data-testid="stFileUploader"] > label { display:none !important; }
[data-testid="stSlider"]       > label { display:none !important; }

/* ── slider — fix warna merah ── */
[data-baseweb="slider"] [role="progressbar"] { background-color:#1565C0 !important; }
[data-baseweb="slider"] [role="slider"] {
    background-color:#1565C0 !important;
    border-color:#1565C0 !important;
    width:18px !important; height:18px !important;
}
[data-baseweb="slider"] > div:first-child { background:#DBEAFE !important; height:4px !important; border-radius:4px; }

/* ── File Uploader (Fix uploadUpload) ───────────────────────────── */
[data-testid="stFileUploaderDropzone"]{
    background:#FFFFFF !important;
    border:1.5px dashed #BFDBFE !important;
    border-radius:10px !important;
    padding:1.25rem 1rem !important;
    text-align:center !important;
    transition:.2s;
}

[data-testid="stFileUploaderDropzone"]:hover{
    border-color:#1565C0 !important;
    background:#F8FBFF !important;
}

[data-testid="stFileUploaderDropzone"] > div{
    display:flex !important;
    flex-direction:column !important;
    align-items:center !important;
    justify-content:center !important;
    gap:.45rem !important;
}

/* ikon */
[data-testid="stFileUploaderDropzone"] svg{
    width:26px !important;
    height:26px !important;
    stroke:#93C5FD !important;
}

/* sembunyikan seluruh tulisan bawaan streamlit */
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small{
    display:none !important;
}

/* tampilkan satu tulisan saja */
[data-testid="stFileUploaderDropzone"]::after{
    content:"📂 Klik untuk upload file CSV";
    color:#1565C0;
    font-size:.9rem;
    font-weight:600;
}

/* hilangkan duplicate upload */
[data-testid="stFileUploaderDropzone"] button{
    opacity:0 !important;
    position:absolute !important;
}
[data-testid="stFileUploaderDropzone"] span { color:#1565C0 !important; font-weight:500 !important; font-size:0.85rem !important; }
[data-testid="stFileUploaderDropzone"] small { color:#93C5FD !important; font-size:0.75rem !important; }
[data-testid="stFileUploaderDropzone"] > div > div:last-child { display:none !important; }
[data-testid="stFileUploaderDropzone"] svg   { width:24px !important; height:24px !important; stroke:#BFDBFE !important; margin-bottom:0.3rem; }

/* ── button — full width, rapi ── */
.stButton > button {
    width:100% !important;
    background:#1565C0 !important;
    color:#FFFFFF !important;
    border:none !important;
    border-radius:10px !important;
    padding:0.68rem 1rem !important;
    font-size:0.9rem !important;
    font-weight:600 !important;
    box-shadow:0 2px 10px rgba(21,101,192,0.22) !important;
    margin-top:0.6rem;
    transition:all 0.2s !important;
    letter-spacing:0.1px;
}
.stButton > button:hover {
    background:#0D47A1 !important;
    box-shadow:0 4px 16px rgba(21,101,192,0.35) !important;
}
.stButton > button:disabled {
    background:#CBD5E1 !important;
    box-shadow:none !important;
    cursor:not-allowed !important;
    color:#94A3B8 !important;
}

/* ── download button ── */
.stDownloadButton > button {
    width:100% !important; background:#FFFFFF !important;
    color:#1565C0 !important; border:1.5px solid #BFDBFE !important;
    border-radius:10px !important; padding:0.6rem 1rem !important;
    font-size:0.87rem !important; font-weight:600 !important; box-shadow:none !important;
}
.stDownloadButton > button:hover { background:#EEF4FF !important; border-color:#1565C0 !important; }

/* ── metric cards ── */
.mrow { display:flex; gap:0.6rem; margin:0.75rem 0 1rem 0; }
.mc   { flex:1; background:#FFFFFF; border:1.5px solid #DBEAFE; border-radius:11px; padding:0.85rem 0.5rem; text-align:center; }
.mc.b { background:#1565C0; border-color:#1565C0; }
.mc.b .ml { color:#BBDEFB; } .mc.b .mv { color:#FFFFFF; }
.ml { color:#7EB3E8; font-size:0.6rem; font-weight:700; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:0.2rem; }
.mv { color:#1565C0; font-size:1.4rem; font-weight:700; line-height:1.1; }
.ms { color:#94A3B8; font-size:0.67rem; margin-top:0.15rem; }
.ms.d { color:#EF4444; font-weight:600; } .ms.g { color:#22C55E; font-weight:600; }

/* ── tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background:#EFF6FF; border-radius:9px; padding:3px;
    border:1.5px solid #DBEAFE; gap:2px;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius:7px !important; color:#64748B !important;
    font-weight:500 !important; font-size:0.8rem !important;
    padding:0.3rem 0.8rem !important; border:none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background:#1565C0 !important; color:#FFFFFF !important; font-weight:600 !important;
}

/* ── radio ── */
[data-testid="stRadio"] > label { display:none !important; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color:#334155 !important; font-size:0.83rem !important; }

/* ── alerts ── */
.stSuccess { background:#EFF6FF !important; border-left:4px solid #1976D2 !important; border-radius:8px !important; }
.stError   { border-left:4px solid #EF4444 !important; border-radius:8px !important; }
.stInfo    { background:#EFF6FF !important; border-left:4px solid #60A5FA !important; border-radius:8px !important; color:#1E40AF !important; }

/* ── dataframe ── */
[data-testid="stDataFrame"] { border:1.5px solid #DBEAFE !important; border-radius:10px !important; overflow:hidden; }

/* ── divider ── */
hr { border-color:#DBEAFE !important; margin:1.2rem 0 !important; }

/* ── footer ── */
.footer { text-align:center; color:#BFDBFE; font-size:0.72rem; margin-top:3rem; padding-top:1rem; border-top:1px solid #DBEAFE; }
</style>
""", unsafe_allow_html=True)

# ── helpers ──────────────────────────────────────────────
@st.cache_resource
def load_model():
    from tensorflow.keras.models import load_model as kl
    return kl("best_hdfs_lstm.keras")

@st.cache_resource
def load_vocab():
    with open("event_to_idx.pkl","rb") as f: return pickle.load(f)

def parse_seq(raw):
    s = str(raw).replace('[','').replace(']','').replace("'","").replace('"','')
    return [e.strip() for e in s.split(',') if e.strip().startswith('E')]

def chart_style(ax):
    ax.set_facecolor('#F8FBFF')
    for sp in ['top','right']: ax.spines[sp].set_visible(False)
    ax.spines['left'].set_color('#DBEAFE'); ax.spines['bottom'].set_color('#DBEAFE')
    ax.tick_params(colors='#64748B', labelsize=7)
    ax.xaxis.label.set_color('#475569'); ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_color('#475569'); ax.yaxis.label.set_size(8)
    ax.title.set_color('#1565C0'); ax.title.set_fontweight('bold'); ax.title.set_fontsize(9)
    ax.grid(color='#DBEAFE', alpha=0.7, linewidth=0.7)

# ── load artifacts ──────────────────────────────────────
try:
    model = load_model()
    vocab = load_vocab()
except FileNotFoundError as e:
    st.error(f"❌ File tidak ditemukan: `{e.filename}`"); st.stop()

# ── HEADER ──────────────────────────────────────────────
st.markdown('<div class="hdr-icon">🔍</div>', unsafe_allow_html=True)
st.markdown('<p class="hdr-title">Deteksi Anomali HDFS</p>', unsafe_allow_html=True)
st.markdown('<p class="hdr-sub">Sistem deteksi anomali log HDFS berbasis Bidirectional LSTM</p>', unsafe_allow_html=True)

# ── THRESHOLD ───────────────────────────────────────────
st.markdown('<div class="sec-lbl">Decision Threshold</div>', unsafe_allow_html=True)
threshold = st.slider("thr", 0.01, 0.99, 0.50, 0.01, label_visibility="collapsed")
st.markdown(f'<p class="sec-hint">Probabilitas ≥ <b>{threshold:.2f}</b> → <b style="color:#EF4444">Anomali</b></p>', unsafe_allow_html=True)
st.markdown('<div class="sec-gap"></div>', unsafe_allow_html=True)

# ── UPLOAD TRACES ───────────────────────────────────────
st.markdown('<div class="sec-lbl">Upload Event Traces</div>', unsafe_allow_html=True)
traces_file = st.file_uploader("traces", type=["csv"], label_visibility="collapsed")
st.markdown('<div class="sec-gap"></div>', unsafe_allow_html=True)

# ── UPLOAD LABEL ─────────────────────────────────────────
st.markdown('<div class="sec-lbl">Anomaly Label &nbsp;<span style="color:#93C5FD;font-weight:400;text-transform:none;letter-spacing:0;font-size:0.73rem">(opsional — untuk evaluasi)</span></div>', unsafe_allow_html=True)
label_file = st.file_uploader("label", type=["csv"], label_visibility="collapsed")
st.markdown('<div class="sec-gap"></div>', unsafe_allow_html=True)

# ── BUTTON ───────────────────────────────────────────────
run = st.button("🔍  Deteksi Anomali", disabled=(traces_file is None))

if traces_file is None:
    st.markdown('<div class="footer">© 2025 Deteksi Anomali HDFS · Bidirectional LSTM</div>', unsafe_allow_html=True)
    st.stop()
if not run:
    st.markdown('<div class="footer">© 2025 Deteksi Anomali HDFS · Bidirectional LSTM</div>', unsafe_allow_html=True)
    st.stop()

# ── PROSES ───────────────────────────────────────────────
df = pd.read_csv(traces_file)
df.columns = [c.strip().lower() for c in df.columns]
if 'blockid' not in df.columns or 'features' not in df.columns:
    st.error("❌ CSV harus punya kolom `blockid` dan `features`."); st.stop()
df['event_list'] = df['features'].apply(parse_seq)

has_label = label_file is not None
if has_label:
    ldf = pd.read_csv(label_file)
    ldf.columns = [c.strip().lower() for c in ldf.columns]
    def slabel(x):
        s = str(x).strip().lower()
        if s in {'normal','success','0','false','benign','-'}: return 0
        if s in {'anomaly','anomalous','abnormal','fail','1','true','attack'}: return 1
        return int(float(s))
    ldf['label_bin'] = ldf['label'].apply(slabel)
    df = pd.merge(df[['blockid','event_list']], ldf[['blockid','label_bin']], on='blockid', how='inner')

with st.spinner("Memproses..."):
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    enc = [[vocab.get(e,0) for e in seq] for seq in df['event_list'].tolist()]
    X   = pad_sequences(enc, maxlen=50, padding='post', truncating='post', value=0)
    probs = model.predict(X, verbose=0).ravel()
    preds = (probs >= threshold).astype(int)

df['anomaly_score'] = probs
df['prediksi']      = preds
df['status']        = df['prediksi'].map({0:'Normal', 1:'🚨 Anomali'})
total=len(df); na=int(preds.sum()); nn=total-na; pa=na/total*100; pn=100-pa

st.success(f"✅ Selesai — {total:,} block diproses.")

# ── METRICS ──────────────────────────────────────────────
st.markdown(f"""
<div class="mrow">
  <div class="mc b"><div class="ml">Total</div><div class="mv">{total:,}</div><div class="ms" style="color:#BBDEFB">Block</div></div>
  <div class="mc"><div class="ml">Normal</div><div class="mv">{nn:,}</div><div class="ms g">▲ {pn:.1f}%</div></div>
  <div class="mc"><div class="ml">Anomali</div><div class="mv" style="color:#EF4444">{na:,}</div><div class="ms d">▲ {pa:.1f}%</div></div>
  <div class="mc"><div class="ml">Threshold</div><div class="mv">{threshold:.2f}</div><div class="ms">Batas</div></div>
</div>
""", unsafe_allow_html=True)

# ── VISUALISASI ───────────────────────────────────────────
BL='#1976D2'; BL2='#64B5F6'; RD='#EF4444'
st.markdown('<div class="sec-lbl" style="margin-top:0.25rem">Visualisasi</div>', unsafe_allow_html=True)
t1,t2,t3 = st.tabs(["Distribusi","Anomaly Score","Evaluasi"])

with t1:
    fig,ax = plt.subplots(1,2,figsize=(7,3),facecolor='#F8FBFF')
    ax[0].pie([nn,na],labels=['Normal','Anomali'],autopct='%1.1f%%',startangle=90,
              explode=(0,0.06),colors=[BL,RD],
              wedgeprops={'edgecolor':'white','linewidth':2},textprops={'fontsize':8,'color':'#334155'})
    ax[0].set_title('Normal vs Anomali',fontsize=9,fontweight='bold',color='#1565C0')
    bars=ax[1].bar(['Normal','Anomali'],[nn,na],color=[BL,RD],edgecolor='white',width=0.42,zorder=3)
    chart_style(ax[1]); ax[1].set_title('Jumlah Block',fontsize=9)
    for b,v in zip(bars,[nn,na]):
        ax[1].text(b.get_x()+b.get_width()/2,b.get_height()+total*0.008,
                   f'{v:,}',ha='center',fontsize=8,fontweight='bold',color='#334155')
    plt.tight_layout(); st.pyplot(fig); plt.close()

with t2:
    fig,ax = plt.subplots(1,2,figsize=(7,3),facecolor='#F8FBFF')
    if has_label:
        ax[0].hist(df.loc[df['label_bin']==0,'anomaly_score'],bins=40,alpha=0.75,label='Normal',color=BL)
        ax[0].hist(df.loc[df['label_bin']==1,'anomaly_score'],bins=40,alpha=0.75,label='Anomali',color=RD)
    else:
        ax[0].hist(df['anomaly_score'],bins=40,color=BL,alpha=0.8)
    ax[0].axvline(threshold,linestyle='--',color='#0D47A1',lw=1.8,label=f'Thr={threshold:.2f}')
    chart_style(ax[0]); ax[0].set_title('Distribusi Score'); ax[0].legend(fontsize=7)
    ni=df[df['prediksi']==0]; ai=df[df['prediksi']==1]
    ax[1].scatter(ni.index,ni['anomaly_score'],s=3,color=BL2,alpha=0.5,label='Normal')
    ax[1].scatter(ai.index,ai['anomaly_score'],s=12,color=RD,marker='x',label='Anomali')
    ax[1].axhline(threshold,linestyle='--',color='#0D47A1',lw=1.5)
    chart_style(ax[1]); ax[1].set_title('Posisi Anomali'); ax[1].legend(fontsize=7)
    plt.tight_layout(); st.pyplot(fig); plt.close()

with t3:
    if not has_label:
        st.info("Upload **anomaly_label.csv** untuk melihat metrik evaluasi.")
    else:
        from sklearn.metrics import (accuracy_score,precision_score,recall_score,
                                     f1_score,roc_auc_score,confusion_matrix,roc_curve)
        yt=df['label_bin'].values; yp=df['anomaly_score'].values; ypr=(yp>=threshold).astype(int)
        acc=accuracy_score(yt,ypr); pre=precision_score(yt,ypr,zero_division=0)
        rec=recall_score(yt,ypr,zero_division=0); f1=f1_score(yt,ypr,zero_division=0)
        auc=roc_auc_score(yt,yp)
        st.markdown(f"""
        <div class="mrow">
          <div class="mc"><div class="ml">Accuracy</div><div class="mv">{acc:.4f}</div></div>
          <div class="mc"><div class="ml">Precision</div><div class="mv">{pre:.4f}</div></div>
          <div class="mc"><div class="ml">Recall</div><div class="mv">{rec:.4f}</div></div>
          <div class="mc"><div class="ml">F1-Score</div><div class="mv">{f1:.4f}</div></div>
          <div class="mc b"><div class="ml">AUC-ROC</div><div class="mv">{auc:.4f}</div></div>
        </div>""", unsafe_allow_html=True)
        fig2,ax2=plt.subplots(1,2,figsize=(7,3),facecolor='#F8FBFF')
        cm=confusion_matrix(yt,ypr)
        sns.heatmap(cm,annot=True,fmt='d',cmap=sns.light_palette('#1565C0',as_cmap=True),
                    xticklabels=['Normal','Anomali'],yticklabels=['Normal','Anomali'],
                    ax=ax2[0],annot_kws={'size':12,'weight':'bold'},linewidths=1,linecolor='white')
        ax2[0].set_title('Confusion Matrix',fontsize=9,fontweight='bold',color='#1565C0')
        ax2[0].set_xlabel('Prediksi',fontsize=8); ax2[0].set_ylabel('Aktual',fontsize=8)
        ax2[0].tick_params(colors='#64748B',labelsize=7)
        fpr,tpr,_=roc_curve(yt,yp)
        ax2[1].plot(fpr,tpr,lw=2,color=BL,label=f'AUC={auc:.4f}')
        ax2[1].fill_between(fpr,tpr,alpha=0.08,color=BL)
        ax2[1].plot([0,1],[0,1],'k--',lw=1,alpha=0.3)
        chart_style(ax2[1]); ax2[1].set_title('ROC Curve')
        ax2[1].set_xlabel('FPR',fontsize=8); ax2[1].set_ylabel('TPR',fontsize=8); ax2[1].legend(fontsize=8)
        plt.tight_layout(); st.pyplot(fig2); plt.close()

# ── TABEL ────────────────────────────────────────────────
st.markdown('<div class="sec-lbl" style="margin-top:1rem">Tabel Hasil</div>', unsafe_allow_html=True)
fo=st.radio("f",["Semua","Anomali saja","Normal saja"],horizontal=True,label_visibility="collapsed")
cols=['blockid','anomaly_score','status']+(['label_bin'] if has_label else [])
dfs=df.copy()
if fo=="Anomali saja": dfs=dfs[dfs['prediksi']==1]
elif fo=="Normal saja": dfs=dfs[dfs['prediksi']==0]
st.dataframe(
    dfs[cols].reset_index(drop=True)
    .style.applymap(
        lambda v:'background-color:#FEE2E2;color:#DC2626;font-weight:600' if v=='🚨 Anomali'
        else ('background-color:#EFF6FF;color:#1565C0' if v=='Normal' else ''),
        subset=['status']
    ).format({'anomaly_score':'{:.4f}'}),
    use_container_width=True, height=320
)
st.markdown("<br>", unsafe_allow_html=True)
st.download_button("⬇️  Download CSV", df[cols].to_csv(index=False).encode(), "hasil_deteksi.csv","text/csv")

st.markdown('<div class="footer">© 2025 Deteksi Anomali HDFS · Bidirectional LSTM</div>', unsafe_allow_html=True)