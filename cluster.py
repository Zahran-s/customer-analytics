import sys
import pandas as pd
from sklearn.cluster import KMeans

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cluster.py <csv-in>")
        return

    in_path = sys.argv[1]
    df = pd.read_csv(in_path)

    num_df = df.select_dtypes(include=['float64','int64'])

    if num_df.shape[1] == 0:
        with open("clusters.txt","w") as f:
            f.write("No numeric columns for clustering.\n")
        return

    kmeans = KMeans(n_clusters=3, n_init='auto')
    labels = kmeans.fit_predict(num_df)

    counts = pd.Series(labels).value_counts().sort_index()

    with open("clusters.txt","w") as f:
        for cluster_id, count in counts.items():
            f.write(f"Cluster {cluster_id}: {count} rows\n")

if __name__ == "__main__":
    main()
