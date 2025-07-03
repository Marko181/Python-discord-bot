from gpt4all import GPT4All
import psutil
from chromadb import Client, PersistentClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# TODO: Set the correct path for model and DBs
CHROMA_DB_DIR = "/home/tinta/Desktop/Python-discord-bot/LLM_finetune/data_scraping/chroma_db"
CHROMA_COLLECTION = "reviews_collection"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TENANT = "default_tenant"
DEFAULT_DATABASE = "default_database"

system_prompt = "You are a Restaurant Review Analyzer, a specialized Large Language Model (LLM) designed to process and analyze restaurant reviews. Your primary task is to take in reviews of restaurants, extract relevant information, and provide enriched responses based on the database specifics. If you do not have data on a given restaurant, say that you do not know."


#client = Client(Settings(anonymized_telemetry=False, persist_directory=CHROMA_DB_DIR))
#print(client.list_collections())
#collection = client.get_collection(CHROMA_COLLECTION)
#embedder = SentenceTransformer(EMBEDDING_MODEL)

class LocalLLM:
    def __init__(self, model_path="mistral-7b-instruct-v0.1.Q4_0.gguf", threads=20):
        print(f"Loading the model: ({model_path})")
        self.model = GPT4All(model_path, n_threads=threads)

    def __call__(self, text_input, num_tokens=50):
        # TODO: add the prompt logic from local_llm
        # Prompt logic and output processing from local_llm
        output_type = "short"
        # Set the flag for text length
        if "--long" in text_input:
            output_type = "long"
            text_input = text_input.replace("--long", "").strip()
            num_tokens = 250
        elif "--raw" in text_input:
            output_type = "raw"
            text_input = text_input.replace("--raw", "").strip()
            num_tokens = 250

        full_input = text_input

        # Edit the input prompt
        if output_type == "short":
            full_input = text_input
        elif output_type == "raw":
            full_input = text_input
        else:
            full_input = text_input

        # Generate the response
        output = self.model.generate(full_input, max_tokens=num_tokens)

        # Handle None, empty strings, or non-string outputs
        if not isinstance(output, str) or not output.strip():
            return "Output is empty or invalid."

        # Find the last period in the string
        last_period_index = output.rfind('.')

        try:
            if output_type == "short":
                end_marker_index = output.find('<end>')
                if end_marker_index != -1:
                    processed_output = output[:end_marker_index].strip()
                else:
                    first_period_index = output.find('.')
                    if first_period_index != -1:
                        processed_output = output[:first_period_index + 1].strip()
                    else:
                        first_newline_index = output.find('\n')
                        if first_newline_index != -1:
                            processed_output = output[:first_newline_index].strip() + "."
                        else:
                            processed_output = output.strip()
            elif output_type == "long":
                if last_period_index != -1:
                    processed_output = output[:last_period_index + 1].strip() + ".."
                else:
                    processed_output = output.strip()
            else:
                processed_output = output.strip()
        except Exception as e:
            processed_output = f"An error occurred in llm.py: {str(e)}"

        if len(processed_output) >= 4000:
            processed_output = processed_output[:3996] + "..."

        return processed_output
        
        
    

# Global LLM instance - only created once, not loading the model every time    
llm_instance = LocalLLM()

def global_llm(text_input, num_tokens):
    return llm_instance(text_input, num_tokens=num_tokens)

def get_resource_stats():
    ##############################################################
    ################# Monitor resource usage #####################
    ##############################################################

    system_stats = f"""
    CPU Usage: {psutil.cpu_percent(interval=1)}%
    Per CPU Usage: {psutil.cpu_percent(interval=1, percpu=True)}

    # Memory utilization
    Total Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB
    Used Memory: {psutil.virtual_memory().used / (1024 ** 3):.2f} GB
    Memory Usage: {psutil.virtual_memory().percent}%

    # Disk utilization
    Total Disk Space: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB
    Used Disk Space: {psutil.disk_usage('/').used / (1024 ** 3):.2f} GB
    Disk Usage: {psutil.disk_usage('/').percent}%

    # Network statistics
    Bytes Sent: {psutil.net_io_counters().bytes_sent / (1024 ** 2):.2f} MB
    Bytes Received: {psutil.net_io_counters().bytes_recv / (1024 ** 2):.2f} MB
    """
    print(system_stats)

    if len(system_stats) >= 4000:
        system_stats = system_stats[:3996] + "..."    

    return system_stats

def local_llm(text_input, threads=20, custom_model="Meta-Llama-3-8B-Instruct.Q4_0.gguf"):

    """
    "orca-mini-3b-gguf2-q4_0.gguf" ali "mistral-7b-instruct-v0.1.Q4_0.gguf"

    "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
    """
    
    output_type = "short"
    num_tokens=50
    
    # Set the flag for text length
    if "--long" in text_input:
        output_type = "long"
        text_input = text_input.replace("--long", "").strip()
        num_tokens = 250
    elif "--raw" in text_input:
        output_type = "raw"
        text_input = text_input.replace("--raw", "").strip()
        num_tokens = 250

    # Select model based on user flag
    if "--fast" in text_input:
        custom_model = "orca-mini-3b-gguf2-q4_0.gguf"
        #custom_model = "mistral-7b-instruct-v0.1.Q4_0.gguf"
    else:
        custom_model = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

    model = GPT4All(custom_model, n_threads=threads)

    # Print out system resource stats
    #get_resource_stats()

    full_input = ""

    # Edit the input prompt
    if output_type == "short" and custom_model == "orca-mini-3b-gguf2-q4_0.gguf":
        full_input = f"Answer this question in one sentance: {text_input}"
        num_tokens = 100
    elif output_type =="short" and custom_model == "Meta-Llama-3-8B-Instruct.Q4_0.gguf":
        #full_input = f"{text_input} After you answer the question write only: <end>"
        full_input = text_input
        #full_input = f"Answer the following question concisely and stop after writing '<end>'. Question: {text_input}"
        #full_input = f"{text_input} <end>"
    elif output_type == "raw":
        full_input = text_input
    else:
        full_input = text_input

    # Generate the response
    output = model.generate(full_input, max_tokens=num_tokens)
    #print("Unedited output: ", output)
    
    # Handle None, empty strings, or non-string outputs
    if not isinstance(output, str) or not output.strip():
        return "Output is empty or invalid."

    # Find the last period in the string
    last_period_index = output.rfind('.')

    try:
        # Check if output is set to short or long
        if output_type == "short":
            # Cut before '<the_end>' if present
            end_marker_index = output.find('<end>')
            if end_marker_index != -1:
                processed_output = output[:end_marker_index].strip()
            else:
                # Fallback: Use the first sentence
                first_period_index = output.find('.')
                if first_period_index != -1:
                    processed_output = output[:first_period_index + 1].strip()
                else:
                    # No period found; fallback to cutting at the first newline
                    first_newline_index = output.find('\n')
                    if first_newline_index != -1:
                        processed_output = output[:first_newline_index].strip()
                        processed_output = processed_output + "."
                    else:
                        # No newline found; return the entire output
                        processed_output = output.strip()
        elif output_type == "long":
            # Keep everything up to the last period
            if last_period_index != -1:
                processed_output = output[:last_period_index + 1].strip()
                processed_output = processed_output + ".."
            else:
                # No period found; return the entire output
                processed_output = output.strip()
        else:
            # Handle unexpected output_type values
            processed_output = output.strip()
    except Exception as e:
        # Catch any unexpected errors
        processed_output = f"An error occurred in llm.py: {str(e)}"

    # Limit the response length to 4000 because of discord message limit
    if len(processed_output) >= 4000:
        processed_output = processed_output[:3996] + "..."
        
    return processed_output

# RAG SECTION START #

# Function loads the chroma collection, currently only supports one collection
# TODO: Expand the function tu support different collections, different types of data
def load_chroma_collection():
    client = PersistentClient(
        path=CHROMA_DB_DIR,
        settings=Settings(anonymized_telemetry=False),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE,
    )
    collection = client.get_collection("reviews_collection")
    return collection

# Retrieve relevant documents from Chroma
def retrieve_documents(collection, query, k=3):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results['documents'][0]

# Load the GPT4All model
def load_gpt4all_model():
    model_path = "mistral-7b-instruct-v0.1.Q4_0.gguf"
    model = GPT4All(model_name=model_path)
    return model


def RAG_answer_pipeline(query, k=5):
    """
    Retrieve relevant reviews and generate an answer using the global LLM instance.
    """
    chroma_collection = load_chroma_collection()
    
    print("collection colected")
    #embedder = SentenceTransformer(EMBEDDING_MODEL)
    #query_embedding = embedder.encode(query).tolist()
    #results = collection.query(query_embeddings=[query_embedding], n_results=k)
    results = retrieve_documents(chroma_collection, query, k=4)
    print("RAG results: ", results)
    #documents = results['documents'][0] if results['documents'] else []
    documents = results[0]['documents'] if results and 'documents' in results[0] else []
    context = "\n".join(documents)
    prompt = (
        f"{system_prompt}\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Please answer in 2-3 sentences, summarizing the main sentiment and key points."
    )
    answer = llm_instance(prompt, num_tokens=500)
    return answer


    
# RAG SECTION END #


