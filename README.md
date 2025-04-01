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
  - Fine-tuning **GPT-4-** with prompt engineering for summarization.  
- **Evaluation metrics**: accuracy, precision, recall, F1-score, elbow method, silhouette score.

---

## 📁  Dataset

- [**Original dataset**: Amazon Product Reviews**](https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products)

These datasets were manually downloaded and combined during the preprocessing step:

1. `.\Dataset\1429_1.csv`  
2. `.\Dataset\Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv`  
3. `.\Dataset\Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv`  

---

##  Data Pipeline

Raw CSV Files (Amazon Reviews)
       │
       ▼
       
 0) Data Preprocessing
     Input:  Raw CSVs
     Output: cleaned_reviews.csv
       │
       ▼

 1) Review Classification
     Input:  cleaned_reviews.csv
     Output: cleaned_reviews_with_sentiment.csv
       │
       ▼

 2) Category Clustering
     Input:  cleaned_reviews_with_sentiment.csv
     Output: full_reviews_with_clusters.csv
       │
       ▼

 3) Review Summarization + Visualization
     Input:  full_reviews_with_clusters.csv
     Output: GPT-4 summaries (.md files), charts

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
