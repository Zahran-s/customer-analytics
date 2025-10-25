import sys
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import numpy as np

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 visualize.py <csv-in>")
        return

    in_path = sys.argv[1]
    df = pd.read_csv(in_path)

    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    hist_col = None
    priority_cols = ["SpendingScore", "AnnualIncome", "Spending_Score", "Income"]

    for c in priority_cols:
        if c in df.columns:
            hist_col = c
            break

    if hist_col is None:
        
        if len(num_cols) > 0:
            hist_col = num_cols[0]

    plt.figure()
    if hist_col is None:
        plt.text(0.5, 0.5, "No numeric columns to visualize", ha='center')
        plt.title("No numeric data")
    else:
        df[hist_col].hist()
        plt.title(f"Distribution of {hist_col}")
        plt.xlabel(hist_col)
        plt.ylabel("Count")

    plt.savefig("summary_plot.png")
    plt.close()

    if len(num_cols) >= 2:
        corr = df[num_cols].corr(numeric_only=True)

        plt.figure()
        plt.imshow(corr, interpolation='nearest')
        plt.title("Correlation Heatmap (numeric features)")
        plt.colorbar()
        plt.xticks(range(len(num_cols)), num_cols, rotation=45, ha='right')
        plt.yticks(range(len(num_cols)), num_cols)
        plt.tight_layout()
        plt.savefig("correlation_heatmap.png")
        plt.close()

    subprocess.run(["python3", "cluster.py", in_path])

if __name__ == "__main__":
    main()

