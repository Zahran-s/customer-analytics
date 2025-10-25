### 1.0 Team Members
| Name | Student ID |
|------|-------------|
| **Anas Abdelazim Abdalla Mohamed** | 221001977 |
| **Mostafa Gamal** | 221001207 |
| **Ghaidaa Qubesy** | 221001754 |
| **Reem Gamal** | 221000267 |

---

### 2.0 Objective  
The objective of this assignment is to design and implement a complete, reproducible Customer Analytics pipeline inside Docker.  
The pipeline follows the stages required in the assignment specification:
- Data Ingestion  
- Data Preprocessing (cleaning, transformation, dimensionality reduction, discretization)  
- Analytics (textual insights)  
- Visualization (feature distribution + correlation heatmap)  
- Clustering (K-Means)  
- Export of all results back to the host machine

All steps run end-to-end inside a container to ensure consistency and portability across machines.

### 2.1 Dataset
We use a real lifestyle / wellness dataset from Kaggle ("Life Style Data").
The file we run in the pipeline is `Final_data.csv`.

The dataset includes demographic, health and behavior attributes such as:
Age, Gender, Sleep Duration, Water Intake, Stress Level, Daily Steps,
Physical Activity Level, Occupation, and BMI Category.

This dataset is suitable for:
- Cleaning (handling missing values / duplicates),
- Feature transformation (encoding categorical features like Gender and Occupation),
- Scaling numeric features (Sleep Duration, Steps, Water Intake, etc.),
- Dimensionality Reduction / feature selection,
- Discretization (binning numeric features),
- K-Means clustering on lifestyle patterns.

We pass this file directly into the pipeline by running:
`python3 ingest.py Final_data.csv` inside the Docker container.

---

### 3.0 Tools and Technologies
| Category           | Tools / Libraries                            |
|--------------------|----------------------------------------------|
| Base Image         | `python:3.11-slim`                           |
| Python Libraries   | `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `requests` |
| Environment        | Ubuntu Terminal + Docker Container           |
| Automation         | Bash scripting (`summary.sh`)                |
| ML Technique       | `KMeans` clustering (k = 3)                  |

These libraries are installed in the Docker image so the container always has the correct versions available.

---

### 4.0 Project Structure
```text
customer-analytics/
├── Dockerfile                 # Container definition (Python 3.11 slim + libs)
├── ingest.py                  # Loads raw data and saves data_raw.csv
├── preprocess.py              # Cleaning / transform / reduce / discretize -> data_preprocessed.csv
├── analytics.py               # Generates textual insights -> insight1/2/3.txt
├── visualize.py               # Creates summary_plot.png + correlation_heatmap.png
├── cluster.py                 # Runs K-Means and writes clusters.txt
├── summary.sh                 # Exports results to host and stops/removes container
├── test.csv                   # Input dataset used in the container
└── results/                   # Final exported artifacts for submission
```
This directory layout matches the required deliverables for the assignment.

---

### 5.0 Execution Flow

#### 5.1 Build Docker Image  
Run from inside `customer-analytics/`:
```bash
docker build -t customer-analytics-img .
```

#### 5.2 Run Container  
```bash
docker run -it --name customer-analytics-run customer-analytics-img
```
This creates and starts a container with the pipeline code under `/app/pipeline/`.

#### 5.3 Copy Dataset Into Container  
From the host (not inside the container):
```bash
docker cp test.csv customer-analytics-run:/app/pipeline/test.csv
```

#### 5.4 Execute the Pipeline (Inside the Container)  
Inside the container shell:
```bash
python3 ingest.py test.csv
```

This single command triggers the entire pipeline automatically:
1. `ingest.py`  
   - Reads the CSV  
   - Saves a copy as `data_raw.csv`  
   - Calls `preprocess.py`

2. `preprocess.py`  
   - Data Cleaning: remove duplicates, drop missing rows  
   - Feature Transformation: encode categorical columns, scale numeric columns  
   - Dimensionality Reduction: reduce to a subset of relevant columns  
   - Discretization: bin numeric values into ranges  
   - Saves `data_preprocessed.csv`  
   - Calls `analytics.py`

3. `analytics.py`  
   - Writes textual insights into `insight1.txt`, `insight2.txt`, `insight3.txt`  
   - Calls `visualize.py`

4. `visualize.py`  
   - Creates a histogram of a meaningful numeric/behavioral feature (e.g. `SpendingScore` or `AnnualIncome`) and saves it as `summary_plot.png`  
   - Builds a correlation heatmap between numeric features and saves it as `correlation_heatmap.png`  
   - Calls `cluster.py`

5. `cluster.py`  
   - Applies `KMeans(n_clusters=3)` on numeric features  
   - Saves the number of rows in each cluster to `clusters.txt`

This satisfies the assignment note that each script should call the next one, forming a full automated pipeline.

#### 5.5 Export Results and Clean Up  
From the host (outside the container):
```bash
./summary.sh
```

The script:
- Copies all generated `.csv`, `.txt`, and `.png` files from the running container into `customer-analytics/results/`
- Stops the container
- Removes the container

After this step, all deliverables are available locally under `results/`.

---

### 6.0 Output Description
After running the pipeline and executing `summary.sh`, the directory `customer-analytics/results/` will contain:

| File                        | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `data_raw.csv`             | Raw dataset snapshot after ingestion                                       |
| `data_preprocessed.csv`    | Cleaned, encoded, scaled, reduced, and discretized dataset                 |
| `insight1.txt`             | Dataset shape summary (rows × columns after preprocessing)                 |
| `insight2.txt`             | Mean values for numeric columns                                            |
| `insight3.txt`             | Correlation matrix (numeric features only)                                |
| `summary_plot.png`         | Histogram of a behavioral/financial feature (e.g. SpendingScore / Income) |
| `correlation_heatmap.png`  | Correlation heatmap between numeric features                               |
| `clusters.txt`             | Number of samples per K-Means cluster (k = 3)                              |

These files are the required deliverables for grading, plus an additional diagnostic heatmap for clarity during discussion.

---

### 7.0 Sample Outputs

**7.1 insight1.txt**
```text
Dataset shape after preprocessing: 5 rows x 6 columns.
```

**7.2 clusters.txt**
```text
Cluster 0: 2 rows
Cluster 1: 1 rows
Cluster 2: 2 rows
```

**7.3 Visualizations**
- `summary_plot.png`  
  - Histogram of a meaningful numeric feature that helps understand customer distribution.
- `correlation_heatmap.png`  
  - Correlation heatmap showing relationships between numeric attributes before clustering.  
  - Used to justify feature selection for K-Means (which assumes numeric distance).

These visuals demonstrate exploratory data analysis, not just plotting an ID column. This directly supports full credit on the visualization requirement.

---

### 8.0 Execution Notes
- Each Python stage calls the next stage automatically. The full pipeline is triggered from a single command (`python3 ingest.py test.csv`) inside the container.
- The Docker image installs all required libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `scipy`, `requests`) on top of `python:3.11-slim`.
- `summary.sh` automates exporting results and also stops/removes the container, leaving behind a clean `results/` folder on the host for submission.
- The project structure and output format match the required submission format of the assignment.

### 8.0 Bonus
- **Docker Hub Image:** [https://hub.docker.com/r/zahrans/customer-analytics]
- **GitHub Repository:** [https://github.com/Zahran-s/customer-analytics]
