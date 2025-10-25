import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 preprocess.py <csv-in>")
        return

    in_path = sys.argv[1]
    df = pd.read_csv(in_path)

    df = df.drop_duplicates()
    df = df.dropna(axis=0)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    for c in cat_cols:
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c].astype(str))

    if numeric_cols:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    cols_to_keep = df.columns[: min(6, len(df.columns))]
    df = df[cols_to_keep]

    if len(cols_to_keep) > 0:
        first_col = df.columns[0]
        try:
            df[first_col + "_binned"] = pd.qcut(df[first_col], q=4, duplicates="drop").astype(str)
        except Exception:
            pass

    df.to_csv("data_preprocessed.csv", index=False)

    subprocess.run(["python3", "analytics.py", "data_preprocessed.csv"])

if __name__ == "__main__":
    main()
