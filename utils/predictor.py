import pandas as pd

from tensorflow.keras.preprocessing.sequence import pad_sequences

from utils.preprocess import parse_seq

def run_prediction(
    csv_file,
    model,
    vocab,
    threshold
):

    df = pd.read_csv(csv_file)

    df.columns = [
        c.strip().lower()
        for c in df.columns
    ]

    df["event_list"] = (
        df["features"]
        .apply(parse_seq)
    )

    encoded = [

        [
            vocab.get(e, 0)
            for e in seq
        ]

        for seq in df["event_list"]
    ]

    X = pad_sequences(
        encoded,
        maxlen=50,
        padding="post",
        truncating="post"
    )

    probs = model.predict(
        X,
        verbose=0
    ).ravel()

    preds = (
        probs >= threshold
    ).astype(int)

    df["anomaly_score"] = probs

    df["status"] = preds

    df["status"] = df["status"].map({
        0: "Normal",
        1: "🚨 Anomali"
    })

    return df[
        [
            "blockid",
            "anomaly_score",
            "status"
        ]
    ]