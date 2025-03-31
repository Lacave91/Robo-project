# **Robo-project** 🤖  
Stop drowning in endless reviews — this model finds the best product for you!  

This project leverages NLP and generative AI to transform scattered Amazon reviews into actionable product recommendations.  
We classify, cluster, and summarize reviews to deliver clear, data-driven suggestions — no more review overload.



[👉 Task Descriptions and Instructions](https://github.com/ironhack-labs/project-nlp-business-case-automated-customers-reviews-v2)

![images/robo - project.png](images/robo-project.png)

---
##  Features

- **Data evaluation**: cleaning and preprocessing text data to optimize model performance.  
- **Model training**:  
  - Using **DistilBERT-base-uncased** and **all-MiniLM-L6-v2** (SentenceTransformers) for embeddings and classification.  
  - Applying **K-Means** for product category clustering.  
  - Fine-tuning **mistralai/Mistral-7B-v0.3** with prompt engineering for summarization.  
- **Evaluation metrics**: accuracy, precision, recall, F1-score, elbow method, silhouette score.

---

##  Dataset

- [**Original dataset**: Amazon Product Reviews**](https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products)

These datasets were manually downloaded and combined during the preprocessing step:

1. `.\Dataset\1429_1.csv`  
2. `.\Dataset\Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv`  
3. `.\Dataset\Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv`  

Place these files into your `data/raw/` directory before running the notebooks.
##  Data Pipeline
|      Step          |      Notebook File                 |        Input File                     |          Output File                       |
|--------------------|------------------------------------|---------------------------------------|--------------------------------------------|
| 1. Preprocessing   | `0)Data_preprocessing.ipynb`       | 'All 3 CSVs listed above              | `.\cleaned_reviews.csv`                    |
| 2. Classification  | `1)Review_Classification.ipynb`    | `.\cleaned_reviews.csv`               | `.\cleaned_reviews_with_sentiment.csv"     |
| 3. Clustering      | `2)CategoryClustering.ipynb`       | `.\reviews_with_sentiment.csv`        | `.\full_reviews_with_clusters.csv`         |
---

## Deployment

---

##  Installation

Use `requirements.txt` to install the required packages. We recommend using a virtual environment.

```bash
python -m venv .venv
.venv/Scripts/activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```
