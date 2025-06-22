from transformers import pipeline
from sentence_transformers import SentenceTransformer
#from rank_bm25 import BM25Okapi
from chromadb import Client
from chromadb.config import Settings
# doesn't work in colab
#from Code.llm import local_llm
from typing import List, Dict, Any
import json
#Test
#Test2

# FOr colab
import sys
sys.path.append('/content/Python-discord-bot/Code/')
from llm import local_llm


# Load the dataset
def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def create_chroma_collection(data, collection_name="reviews_collection"):
    # Initialize Chroma client (in-memory)
    client = Client(Settings(anonymized_telemetry=False))
    # Create or get collection
    collection = client.get_or_create_collection(collection_name)
    # Prepare documents and embeddings
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    reviews = [item["review"] for item in data if "review" in item]
    embeddings = embedder.encode(reviews).tolist()
    # Add documents to Chroma
    collection.add(
        documents=reviews,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(reviews))],
        # Adding the metadata for additional context retrieval,
        metadatas=[{"reviewer": item["reviewer"], "rating": item["rating"], "restaurant": item["restaurant"]} for item in data if "review" in item]
    )
    return collection, reviews, embedder

def retrieve_reviews_vector(query, collection, embedder, top_k=3):
    query_embedding = embedder.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    # results['documents'] is a list of lists (one per query)
    return results['documents'][0] if results['documents'] else []


"""# Preprocess and index documents
def create_bm25_index(data: List[Dict[str, Any]]):
    # Extract reviews
    reviews = [item["review"] for item in data]

    # Tokenize the reviews
    tokenized_reviews = [review.split() for review in reviews]

    # Create BM25 index
    bm25 = BM25Okapi(tokenized_reviews)
    return bm25, reviews"""

# Retrieve relevant reviews
def retrieve_reviews(query: str, bm25_index, reviews: List[str], top_k: int = 3):
    tokenized_query = query.split()
    doc_scores = bm25_index.get_scores(tokenized_query)
    top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
    return [reviews[i] for i in top_indices]


# Generate answer using a text generation pipeline
"""def generate_answer(query: str, retrieved_reviews: List[str]) -> str:
    prompt = (
        f"Based on the following restaurant reviews:\n"
        f"{' '.join(retrieved_reviews)}\n\n"
        f"Answer the following question: {query}\n"
    )

    # Initialize the text generation pipeline
    generator = pipeline("text-generation", model="distilgpt2")

    # Generate answer
    answer = generator(prompt, max_length=500, num_return_sequences=1, truncation=True)[0]['generated_text']
    return answer
"""
# V primeru uporabe LLMja iz gpt4all iz llm.py
def generate_answer(query: str, retrieved_reviews: List[str]) -> str:
    prompt = (
        f"Based on the following restaurant reviews:\n"
        f"{' '.join(retrieved_reviews)}\n\n"
        f"Answer the following question: {query}\n"
    )

    # Use your local LLM instead of Hugging Face pipeline
    answer = local_llm(prompt)
    # Bolj natančen klic
    #answer = local_llm(prompt, custom_model="Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    return answer

# Main function to answer a query
def answer_question(query: str, data: List[Dict[str, Any]]):
    collection, reviews, embedder = create_chroma_collection(data)
    retrieved_reviews = retrieve_reviews_vector(query, collection, embedder)
    if not retrieved_reviews:
        return "No relevant reviews found."
    answer = generate_answer(query, retrieved_reviews)
    return answer

# Example usage
if __name__ == "__main__":
    #data_file = 'Code/LLM_finetune/data_scraping/restaurant_reviews_V2.json'
    # Colab version
    data_file = '/content/Python-discord-bot/Code/LLM_finetune/data_scraping/restaurant_reviews_V2.json'
    data = load_json_data(data_file)
    print("Querying the question")
    query = "Give me the general impression and sentiment about the Foculus restaurant based on the reviews."
    answer = answer_question(query, data)
    print(answer)