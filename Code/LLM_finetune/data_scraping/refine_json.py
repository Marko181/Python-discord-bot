import json

# Load your original dataset
with open("/Users/lukamelinc/Desktop/Programiranje/Python-discord-bot/Code/LLM_finetune/data_scraping/restaurant_reviews.json", "r", encoding="utf-8") as f:
    reviews = json.load(f)

# Convert to the correct format
formatted_data = []
for review in reviews:
    formatted_data.append({"text": f"{review['reviewer_name']} rated {review['restaurant_name']} {review['rating']} stars: '{review['review_text']}'"})

# Save formatted dataset
with open("/Users/lukamelinc/Desktop/Programiranje/Python-discord-bot/Code/LLM_finetune/data_scraping/restaurant_reviews.json", "w", encoding="utf-8") as f:
    json.dump(formatted_data, f, indent=4, ensure_ascii=False)

print("Dataset formatted for fine-tuning!")
