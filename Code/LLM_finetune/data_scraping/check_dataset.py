import sqlite3

DB_NAME = "tripadvisor_reviews.db"

# Connect to the database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Query the first 5 reviews
cursor.execute("SELECT * FROM reviews LIMIT 5")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
