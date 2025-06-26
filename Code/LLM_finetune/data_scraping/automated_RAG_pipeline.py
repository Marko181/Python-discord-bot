import os
import sys
import time
import json



# Make sure all scripts are importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data_scraping'))
sys.path.append('/content/Python-discord-bot/Code/LLM_finetune/data_scraping')

from scraping_google import create_database, scrape_google_reviews, read_restaurant_list

# --- Step 1: Read restaurant list --- #

# Non-Colab paths
RESTAURANTS_TXT = 'restaurants.txt'
DB_PATH = 'google_reviews.db'
JSON_EXPORT_PATH = 'data/restaurant_reviews_V2.json'
CHROMA_DB_DIR = 'chroma_db'

# Colab paths
# TODO
#RESTAURANTS_TXT = '/content/restaurants.txt'
#DB_PATH = '/content/google_reviews.db'
#JSON_EXPORT_PATH = '/content/restaurant_reviews_V2.json'
#CHROMA_DB_DIR = '/content/chroma_db'

# --- Step 2: Scrape reviews and save to DB ---
def scrape_all_restaurants():
    create_database()
    restaurant_list = read_restaurant_list(RESTAURANTS_TXT)
    for restaurant_name in restaurant_list:
        print(f"Scraping: {restaurant_name}")
        scrape_google_reviews(restaurant_name, num_reviews=20)
        time.sleep(10)  # To avoid detection/rate-limiting

# --- Step 3: Export reviews from DB to JSON ---
def export_reviews_to_json():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT restaurant_name, reviewer_name, rating, review_date, review_text FROM reviews")
    rows = cursor.fetchall()
    conn.close()
    # Format for RAG
    data = []
    for row in rows:
        data.append({
            "restaurant": row[0],
            "reviewer": row[1],
            "rating": row[2],
            "date": row[3],
            "review": row[4]
        })
    os.makedirs(os.path.dirname(JSON_EXPORT_PATH), exist_ok=True)
    with open(JSON_EXPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(data)} reviews to {JSON_EXPORT_PATH}")

# --- Step 4: Build Chroma vector DB ---
def build_chroma_vector_db():
    from chromadb import Client
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer

    with open(JSON_EXPORT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    client = Client(Settings(anonymized_telemetry=False, persist_directory=CHROMA_DB_DIR))
    collection = client.get_or_create_collection("reviews_collection")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    reviews = [item["review"] for item in data if "review" in item]
    embeddings = embedder.encode(reviews).tolist()
    collection.add(
        documents=reviews,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(reviews))]
    )
    print(f"Chroma vector DB built with {len(reviews)} reviews at {CHROMA_DB_DIR}")



# --- Main orchestrator ---
if __name__ == "__main__":
    print("Step 1 & 2: Scraping all restaurants...")
    scrape_all_restaurants()
    print("Step 3: Exporting reviews to JSON...")
    export_reviews_to_json()
    print("Step 4: Building Chroma vector DB...")
    build_chroma_vector_db()
    print("Pipeline complete!")