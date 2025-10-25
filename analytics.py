import sys
import pandas as pd
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analytics.py <csv-in>")
        return

    in_path = sys.argv[1]
    df = pd.read_csv(in_path)

    insight1 = f"Dataset shape after preprocessing: {df.shape[0]} rows x {df.shape[1]} columns."
    insight2 = "Column means (numeric):\n" + df.mean(numeric_only=True).to_string()
    insight3 = "Correlation matrix (numeric):\n" + df.corr(numeric_only=True).to_string()

    with open("insight1.txt", "w") as f: f.write(insight1)
    with open("insight2.txt", "w") as f: f.write(insight2)
    with open("insight3.txt", "w") as f: f.write(insight3)

    subprocess.run(["python3", "visualize.py", in_path])

if __name__ == "__main__":
    main()
