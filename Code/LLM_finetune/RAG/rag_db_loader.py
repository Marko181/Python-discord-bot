import json
from datasets import load_dataset
from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
from langchain.schema import Document
#from langchain.vectorstores import BM25
#from llm import local_llm
from smolagents import CodeAgent, InferenceClientModel
from transformers import pipeline


# Load the dataset
data = load_dataset('json', data_files='Code/LLM_finetune/data_scraping/restaurant_reviews_V2.json')
# Convert the dataset into a format compatible with BM25Retriever
documents = [
    Document(
        page_content=item["review"],
        metadata={
            "reviewer": item["reviewer"],
            "rating": item["rating"],
            "restaurant": item["restaurant"]
        }
    )
    for item in data["train"]
]

# Create a BM25 index
#bm25_index = BM25Index.from_document(documents)

# BM25 retriever instance
# DB has keys: reviewer, ranking, review, restaurant so we specify text_key="review" to let BM25 index the reviews
retriever = BM25Retriever.from_documents(documents)

generator = pipeline("text-generation", model="distilgpt2")

def generate_answer(query: str, reviewed_text: str) -> str:
    """
    Construct a prompt that includes the retrieved reviews text and the question,
    then pass it to the LLM for generating an answer.
    """

    prompt = (
       #f"Based on the following restaurant reviews:\n{reviewed_text}\n\n"
       #f"Answer the following question: {query}\n"
       f"Based on the following restaurant reviews:\n{reviewed_text}\n\n"
       f"Answer the following question: {query}\n"
    )

    # Use the smolagents to generate an answer
    answer = generator(prompt, max_length=500, num_return_sequences=1, truncation=True)[0]['generated_text']
    return answer

def answer_question(query: str) -> str:
    "Retrieve the most relevant reviews for the user query and generate an answer."

    # REtruieve relevant docs(reviews)
    docs = retriever.invoke(input=query)
    if not docs:
        return "No relevant reviews found."
    
    combined_reviews = "\n".join([doc.page_content for doc in docs])

    answer = generate_answer(query, combined_reviews)

    return answer

class RestaurantReviewRAG(Tool):
    name = "restaurant_review_rag"
    description = (
        "This tool retrieves restaurant reviews for a given query about the restaurant and "
        "generates an answer using a retrieval-augmented generation (RAG) approach."
    )

    def run(self, query: str) -> str:
        return answer_question(query)

def main():
    #query = "Tell me about the reviews of the Foculus restaurant."
    query = "Give me the general impression and sentiment about the Foculus restaurant based on the reviews."
    answer = answer_question(query)
    print(answer)

if __name__ == "__main__":
    main()