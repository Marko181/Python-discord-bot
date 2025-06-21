from transformers import pipeline
from rank_bm25 import BM25Okapi
from typing import List, Dict, Any
import json

# Load the dataset
def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Preprocess and index documents
def create_bm25_index(data: List[Dict[str, Any]]):
    # Extract reviews
    reviews = [item["review"] for item in data]

    # Tokenize the reviews
    tokenized_reviews = [review.split() for review in reviews]

    # Create BM25 index
    bm25 = BM25Okapi(tokenized_reviews)
    return bm25, reviews

# Retrieve relevant reviews
def retrieve_reviews(query: str, bm25_index, reviews: List[str], top_k: int = 3):
    tokenized_query = query.split()
    doc_scores = bm25_index.get_scores(tokenized_query)
    top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
    return [reviews[i] for i in top_indices]


# Generate answer using a text generation pipeline
def generate_answer(query: str, retrieved_reviews: List[str]) -> str:
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

# Main function to answer a query
def answer_question(query: str, data: List[Dict[str, Any]]):
    bm25_index, reviews = create_bm25_index(data)
    retrieved_reviews = retrieve_reviews(query, bm25_index, reviews)
    if not retrieved_reviews:
        return "No relevant reviews found."
    answer = generate_answer(query, retrieved_reviews)
    return answer

# Example usage
if __name__ == "__main__":
    data_file = 'Code/LLM_finetune/data_scraping/restaurant_reviews_V2.json'
    data = load_json_data(data_file)
    query = "Give me the general impression and sentiment about the Foculus restaurant based on the reviews."
    answer = answer_question(query, data)
    print(answer)