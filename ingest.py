import sys
import pandas as pd
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ingest.py <dataset-path>")
        return

    src_path = sys.argv[1]

    df = pd.read_csv(src_path)
    df.to_csv("data_raw.csv", index=False)

    subprocess.run(["python3", "preprocess.py", "data_raw.csv"])

if __name__ == "__main__":
    main()

