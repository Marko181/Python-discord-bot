from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import sys
sys.path.append('/content/Python-discord-bot/Code/')
from llm import local_llm, global_llm  # or your LLM import

client = Client(Settings(anonymized_telemetry=False, persist_directory="chroma_db"))
collection = client.get_collection("reviews_collection")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_reviews_vector(query, collection, embedder, top_k=3):
    query_embedding = embedder.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results['documents'][0] if results['documents'] else []

def generate_answer(query, retrieved_reviews):
    prompt = (
        f"Based on the following restaurant reviews:\n"
        f"{' '.join(retrieved_reviews)}\n\n"
        f"Answer the following question: {query}\n"
    )
    #return local_llm(prompt)
    return global_llm(prompt, num_tokens=300)

# Example usage
query = "Give me the general impression and sentiment about the Foculus restaurant based on the reviews."
print("Retrieving the data")
retrieved_reviews = retrieve_reviews_vector(query, collection, embedder)
print("Generating the data")
answer = generate_answer(query, retrieved_reviews)
print(answer)