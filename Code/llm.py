from gpt4all import GPT4All
import psutil

class LocalLLM:
    def __init__(self, model_path="Meta-Llama-3-8B-Instruct.Q4_0.gguf", threads=20):
        print(f"Loading the model: ({model_path})")
        self.model = GPT4All(model_path, n_threads=threads)

    def __call__(self, text_input, num_tokens=50):
        # TODO: add the prompt logic from local_llm
        output = self.model.generate(text_input, max_tokens=num_tokens)
        return output
    

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
    "orca-mini-3b-gguf2-q4_0.gguf"

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
    else:
        custom_model = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

    model = GPT4All(custom_model, n_threads=threads)

    # Print out system resource stats
    get_resource_stats()

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

if __name__ == "__main__":
    text = input("Write your question here: ")
    output = local_llm(text, custom_model="Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    print(output)