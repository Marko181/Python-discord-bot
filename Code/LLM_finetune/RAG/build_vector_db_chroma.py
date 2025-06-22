from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json

# Load data
# TODO: change the path to the database for Colab
# with open('/content/Python-discord-bot/Code/LLM_finetune/data_scraping/restaurant_reviews_V2.json', 'r') as f:
with open('data/restaurant_reviews_V2.json', 'r') as f:
    data = json.load(f)

client = Client(Settings(anonymized_telemetry=False, persist_directory="chroma_db"))
collection = client.get_or_create_collection("reviews_collection")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

reviews = [item["review"] for item in data if "review" in item]
embeddings = embedder.encode(reviews).tolist()
collection.add(
    documents=reviews,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(reviews))]
)
#client.persist()