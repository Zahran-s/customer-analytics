mkdir -p ./results

docker cp customer-analytics-run:/app/pipeline/data_raw.csv ./results/
docker cp customer-analytics-run:/app/pipeline/data_preprocessed.csv ./results/
docker cp customer-analytics-run:/app/pipeline/insight1.txt ./results/
docker cp customer-analytics-run:/app/pipeline/insight2.txt ./results/
docker cp customer-analytics-run:/app/pipeline/insight3.txt ./results/
docker cp customer-analytics-run:/app/pipeline/summary_plot.png ./results/
docker cp customer-analytics-run:/app/pipeline/correlation_heatmap.png ./results/
docker cp customer-analytics-run:/app/pipeline/clusters.txt ./results/

docker stop customer-analytics-run
docker rm customer-analytics-run
