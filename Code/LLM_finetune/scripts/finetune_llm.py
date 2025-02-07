import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
from trl import SFTTrainer
import os

# Model and paths
BASE_MODEL = "mistralai/Mistral-7B-v0.1"
OUTPUT_MODEL = "./models/fine_tuned_model"
DATASET_PATH = "./data/restaurant_reviews.json"  # Updated path

os.makedirs(OUTPUT_MODEL, exist_ok=True)



# 4-bit quantization with BitsAndBytes
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

print("Loading model...")
# Load model with quantization config
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL, 
    device_map="auto", 
    torch_dtype=torch.float16,
    quantization_config=bnb_config
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token  # Add padding token

# Load dataset
dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

# LoRA Configuration
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]
)

# Apply QLoRA
model = get_peft_model(model, config)
model.print_trainable_parameters()

# Training arguments for fine-tuning
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    optim="paged_adamw_8bit",
    num_train_epochs=3,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    output_dir=OUTPUT_MODEL,
    logging_steps=10,
    learning_rate=2e-4,
    weight_decay=0.01,
    fp16=True  # Change to `bf16=True` if needed
)

# Fine-tune the model
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer
)

print("Starting the training...")
trainer.train()

# Save the fine-tuned model
trainer.save_model(OUTPUT_MODEL)
print("Tuned model saved at:", OUTPUT_MODEL)
