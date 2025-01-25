from gpt4all import GPT4All
import psutil

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

    full_input = ""

    # Edit the input prompt
    if output_type == "short" and custom_model == "orca-mini-3b-gguf2-q4_0.gguf":
        full_input = f"Answer this question in one sentance: {text_input}"
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

    ##############################################################
    ################# Monitor resource usage #####################
    ##############################################################

    # CPU utilization
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
    print(f"Per CPU Usage: {psutil.cpu_percent(interval=1, percpu=True)}")

    # Memory utilization
    memory = psutil.virtual_memory()
    print(f"Total Memory: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Used Memory: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Memory Usage: {memory.percent}%")

    # Disk utilization
    disk = psutil.disk_usage('/')
    print(f"Total Disk Space: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Used Disk Space: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Disk Usage: {disk.percent}%")

    # Network statistics
    net = psutil.net_io_counters()
    print(f"Bytes Sent: {net.bytes_sent / (1024 ** 2):.2f} MB")
    print(f"Bytes Received: {net.bytes_recv / (1024 ** 2):.2f} MB")

    ##############################################################
    ############# End of monitoring resource usage ###############
    ##############################################################
    
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
        processed_output = f"An error occurred: {str(e)}"

    # Limit the response length to 4000 because of discord message limit
    if len(processed_output) >= 4000:
        processed_output = processed_output[:3996] + "..."
        
    return processed_output

if __name__ == "__main__":
    text = input("Write your question here: ")
    output = local_llm(text, custom_model="Meta-Llama-3-8B-Instruct.Q4_0.gguf")
    print(output)