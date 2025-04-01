import re
import openai

# === Clean product name ===
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

# === Get top 3 products per category ===
def get_top_3_products(df, min_reviews=50):
    product_stats = df.groupby(['cluster_name', 'clean_name']).agg(
        review_count=('review', 'count'),
        average_rating=('reviews.rating', 'mean')
    ).reset_index()
    filtered = product_stats[product_stats['review_count'] >= min_reviews]
    sorted_products = filtered.sort_values(
        by=['cluster_name', 'average_rating', 'review_count'],
        ascending=[True, False, False]
    )
    return sorted_products.groupby('cluster_name').head(3)

# === Get worst-rated product per category ===
def get_worst_product(df, min_reviews=50):
    product_stats = df.groupby(['cluster_name', 'clean_name']).agg(
        review_count=('review', 'count'),
        average_rating=('reviews.rating', 'mean')
    ).reset_index()
    filtered = product_stats[product_stats['review_count'] >= min_reviews]
    sorted_products = filtered.sort_values(
        by=['cluster_name', 'average_rating', 'review_count'],
        ascending=[True, True, False]
    )
    return sorted_products.groupby('cluster_name').head(1)

# === Generate summary with GPT-4 ===
def summarize_category(category, df, top_3, worst_products, max_tokens_per_product=1000):
    prompt = f"""
You are a professional product review writer creating a blog-style article for a tech-savvy audience (like The Verge or Wirecutter).

Your task is to:
- Compare the **top 3 Amazon {category.lower()}s** based on real customer feedback
- Include a short, informative paragraph for each product:
    - What customers liked 
    - What customers complained about 
    - What makes it unique
- Add 2 bullet points at the end of each paragraph:
    - **Pros**
    - **Cons**
- Finish with a final paragraph about the **worst-rated {category.lower()}**, including:
    - Why it scored lower
    - What users complained about
    - Why readers should consider avoiding it

Write in a clear, helpful, and slightly conversational tone. Format the article using markdown with product names as headings.

Here are the reviews:
"""

    review_text = ""

    top_names = top_3[top_3['cluster_name'] == category]['clean_name'].tolist()
    worst_name = worst_products[worst_products['cluster_name'] == category]['clean_name'].values[0]

    for product in top_names + [worst_name]:
        product_reviews = df[
            (df['cluster_name'] == category) & (df['clean_name'] == product)
        ]['review'].tolist()

        if product_reviews:
            display_name = df[
                (df['clean_name'] == product) & (df['cluster_name'] == category)
            ]['name'].value_counts().idxmax()
        else:
            display_name = product.title()

        joined = " ".join(product_reviews)[:max_tokens_per_product * 4]
        review_text += f"\n\n## {display_name}\n\n{joined.strip()}\n"

    full_prompt = prompt + review_text.strip()
    response = generate_with_gpt4(full_prompt)
    return response

# === GPT-4 OpenAI call ===
def generate_with_gpt4(prompt, model="gpt-4", max_tokens=1000, temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful product reviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response['choices'][0]['message']['content'].strip()