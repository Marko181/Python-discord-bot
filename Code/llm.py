from gpt4all import GPT4All
import psutil


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
    temperature = 0.1   # default temperature

    # Check if temperature flag is present
    temp_flag_index = text_input.find("--temperature=")
    if temp_flag_index == -1:
        temp_flag_index = text_input.find("--temperatura=")

    if temp_flag_index != -1:
        # Start of the temperature value just after "="
        start_index = temp_flag_index + (len("--temperature=") if temp_flag_index == text_input.find("--temperature=") else len("--temperatura="))
        end_index = text_input.find(" ", start_index)

        if end_index == -1:  # If no spaces after the value, use the end of the string
            end_index = len(text_input)

        try:

            # Extract the temperature value and convert it to float
            temperature = float(text_input[start_index:end_index])

            if temperature > 0.99 or temperature < 0:
                return "Error: Temperature value must be between 0 and 0.99."
        except ValueError:
            return "Error: Invalid temperature value."

        # Remove the temperature part from the input string
        text_input = text_input[:temp_flag_index].strip() + ' ' + text_input[end_index:].strip()

    
    
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

    model = GPT4All(custom_model, n_threads=threads, temperature=temperature)

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