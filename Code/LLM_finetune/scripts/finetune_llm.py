import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
from trl import SFTTrainer
import os

# TODO
BASE_MODEL = "mistralai/Mistral-7B-v0.1"
OUTPUT_MODEL = "./models/fine_tuned_model"
DATASET_PATH = "./data/TODO"

os.makedirs(OUTPUT_MODEL, exist_ok=True)


print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

# 4-bit quantization with BitsAndBytes
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,   # 4bit quantization
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,        # Hyperparameter fine tuninga
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"]     # odvisno od modela
)

# QLoRA to the model
model = get_peft_model(model, config)
model.print_trainable_parameters()

# Training arguments for fine tuning
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
    fp16=True 
)

# Fine tuning the model
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer
)

print("Starting the training...")
trainer.train()

# Saving the tuned model
trainer.save_model(OUTPUT_MODEL)
print("Tuned model saved")