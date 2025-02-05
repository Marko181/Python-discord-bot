import sqlite3
import json
import os

DB_NAME = "restaurant_reviews.db"
OUTPUT_JSON = "restaurant_reviews.json"

def export_reviews_to_json():
    """Exports all restaurant reviews from SQLite database to a JSON file."""
    
    # Check if database exists
    if not os.path.exists(DB_NAME):
        print(f"Database {DB_NAME} not found.")
        return

    # Connect to database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch all reviews
    cursor.execute("SELECT restaurant_name, reviewer_name, rating, review_date, review_text FROM reviews")
    reviews = cursor.fetchall()

    # Convert data into a structured JSON format
    reviews_data = []
    for review in reviews:
        review_entry = {
            "restaurant_name": review[0],
            "reviewer_name": review[1],
            "rating": review[2],
            "review_date": review[3],
            "review_text": review[4]
        }
        reviews_data.append(review_entry)

    # Save to JSON file
    with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
        json.dump(reviews_data, json_file, indent=4, ensure_ascii=False)

    # Close database connection
    conn.close()

    print(f"Successfully exported {len(reviews_data)} reviews to {OUTPUT_JSON}")

# Run export function
if __name__ == "__main__":
    export_reviews_to_json()
