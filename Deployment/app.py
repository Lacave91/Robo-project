import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# === Load Data ===
@st.cache_data
def load_data():
    script_dir = os.path.dirname(__file__)  # Get folder where app.py is

    df = pd.read_csv(os.path.join(script_dir, "full_reviews_with_clusters.csv"))

    summaries_path = os.path.join(script_dir, "summaries_clean")
    summary_files = {
        file.replace("_summary.md", "").replace("_", " ").title(): os.path.join(summaries_path, file)
        for file in os.listdir(summaries_path) if file.endswith(".md")
    }

    return df, summary_files

# Load it
df, summary_files = load_data()

def clean_product_name(name):
    name = name.lower()
    name = re.sub(r'\b(black|blue|pink|silver|marine|tangerine|magenta|white|red|yellow|green|purple|gold|gray|grey|orange|rose|charcoal|graphite|plum|teal|lavender|coral)\b', '', name)
    name = re.sub(r'\b(all-new|includes special offers|includes offers|with special offers|with alexa)\b', '', name)
    name = re.sub(r'\b\d+\s?gb\b', '', name)
    name = re.sub(r'\b(5th|6th|7th|8th|9th|10th|11th|12th)\s?gen(eration)?\b', '', name)
    name = re.sub(r'\bwi[-]?fi\b|\bdisplay\b', '', name)
    name = re.sub(r'[^\w\s\-"]+', '', name)
    name = re.sub(r'(tablet)[^a-zA-Z]*(tablet)', r'\1', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

# Apply it to create the missing column
df["clean_name"] = df["name"].apply(clean_product_name)

# === Sidebar ===
st.sidebar.title("📂 Product Category")
categories = sorted(df['cluster_name'].unique())
selected_category = st.sidebar.selectbox("Choose a category:", categories)

# === Main Content ===
st.title("📊 Product Review Summary Dashboard")
st.markdown(f"### Category: **{selected_category}**")

# === Sentiment Distribution ===
sentiment_counts = df[df['cluster_name'] == selected_category]['sentiment'].value_counts()
st.subheader("Sentiment Distribution")
fig, ax = plt.subplots()
ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# === Top & Worst Products Table ===
top_products = df[df['cluster_name'] == selected_category].groupby('clean_name').agg(
    avg_rating=('reviews.rating', 'mean'),
    review_count=('review', 'count')
).reset_index().sort_values(by=['avg_rating', 'review_count'], ascending=[False, False])

st.subheader("🔝 Top 3 Products")
st.dataframe(top_products.head(3).reset_index(drop=True))

st.subheader("⛔ Worst Rated Product")
st.dataframe(top_products.tail(1).reset_index(drop=True))

# === Markdown Summary ===
st.subheader("📝 Summary Article")
summary_key = selected_category.lower().replace(" ", "_").replace("&", "and").replace("(", "").replace(")", "")
summary_filename = f"{summary_key}_summary.md"
summary_path = os.path.join("summaries_clean", summary_filename)

if os.path.exists(summary_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()

    # 🔧 Auto-fix: Add heading to worst-rated section if missing
    if "worst-rated" in summary_text.lower() and "## " not in summary_text.lower().split("worst-rated")[1][:100]:
        # Extract worst product name from last table row
        worst_product_name = top_products.tail(1)["clean_name"].values[0].replace("-", " ").title()
        # Inject heading just before the worst-rated paragraph
        summary_text = summary_text.replace(
            "For users seeking the worst-rated",
            f"## ⚠️ Worst Rated Product: {worst_product_name}\n\nFor users seeking the worst-rated"
        )

    st.markdown(summary_text)
else:
    st.warning("Summary not available for this category.")
