import gradio as gr
import pandas as pd
import json
import os
from dotenv import load_dotenv
import openai

from pipeline import (
    summarize_category  # Only needed if using GPT-4 live
)

# === Load environment variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Load processed data ===
df = pd.read_csv(r"C:\Users\alvar\OneDrive\文件\Iron Hack\Product Review project\Deployment\data\df_cleaned.csv")
top_3 = pd.read_csv(r"C:\Users\alvar\OneDrive\文件\Iron Hack\Product Review project\Deployment\data\top_3.csv")
worst_products = pd.read_csv(r"C:\Users\alvar\OneDrive\文件\Iron Hack\Product Review project\Deployment\data\worst_products.csv")

# === Option A: Load pre-generated summaries (faster, no GPT call)
with open(r"C:\Users\alvar\OneDrive\文件\Iron Hack\Product Review project\Deployment\summaries\all_summaries.json", "r", encoding="utf-8") as f:
    precomputed_summaries = json.load(f)

def generate_summary(category):
    return precomputed_summaries.get(category, "❌ No summary available for this category.")

# === Option B: GPT-4 Live (uncomment below and comment Option A to use GPT live) ===
# def generate_summary(category):
#     return summarize_category(category, df, top_3, worst_products)

# === Set up categories ===
categories = sorted(df["cluster_name"].unique())

# === Build Gradio UI ===
demo = gr.Interface(
    fn=generate_summary,
    inputs=gr.Dropdown(choices=categories, label="Select a Product Category"),
    outputs=gr.Markdown(label="📄 GPT-4 Summary"),
    title="🛍️ Amazon Product Review Summarizer",
    description="AI-generated product recommendations based on real customer reviews. Select a category to explore."
)

if __name__ == "__main__":
    demo.launch(share=True)
