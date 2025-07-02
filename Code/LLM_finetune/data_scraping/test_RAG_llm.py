from chromadb import PersistentClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from gpt4all import GPT4All

# Load the Chroma collection
CHROMA_DB_DIR = "/home/tinta/Desktop/Python-discord-bot/LLM_finetune/data_scraping/chroma_db"
DEFAULT_TENANT = "default_tenant"
DEFAULT_DATABASE = "default_database"

def load_chroma_collection():
    client = PersistentClient(
        path=CHROMA_DB_DIR,
        settings=Settings(anonymized_telemetry=False),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    collection = client.get_collection("reviews_collection")
    return collection

# Load the GPT4All model
def load_gpt4all_model():
    model_path = "mistral-7b-instruct-v0.1.Q4_0.gguf"
    model = GPT4All(model_name=model_path)
    return model

# Retrieve relevant documents from Chroma
def retrieve_documents(collection, query, k=3):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results['documents'][0]

# Generate response using GPT4All
def generate_response(model, prompt):
    output = model.generate(prompt=prompt)
    return output

# Integrate retrieval and LLM into a simple pipeline
def query_pipeline(query):
    # Load the Chroma collection and GPT4All model
    collection = load_chroma_collection()
    model = load_gpt4all_model()

    # Retrieve relevant documents
    documents = retrieve_documents(collection, query)
    context = "\n".join(documents)

    # Generate prompt for GPT4All
    prompt = f"Context:\n{context}\n\nQuery:\n{query}\n\nAnswer the query based on the provided context:"
    response = generate_response(model, prompt)

    return response

# Test the pipeline
if __name__ == "__main__":
    query = "What are some positive reviews about Pizzeria FoculuS?"
    response = query_pipeline(query)
    print("Response:", response)