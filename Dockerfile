FROM python:3.11-slim

RUN pip install --no-cache-dir pandas numpy matplotlib seaborn scikit-learn scipy requests

WORKDIR /app/pipeline/

COPY ingest.py preprocess.py analytics.py visualize.py cluster.py README.md /app/pipeline/

CMD ["/bin/bash"]

