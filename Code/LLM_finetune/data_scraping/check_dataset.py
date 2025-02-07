import sqlite3

DB_NAME = "google_reviews.db"

# Connect to the database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Query the first 5 reviews
cursor.execute("SELECT * FROM reviews LIMIT 20")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

print(len(rows))
# Close the connection
conn.close()
