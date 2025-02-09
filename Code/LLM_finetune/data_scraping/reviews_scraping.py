from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import time

# Database setup
DB_NAME = "tripadvisor_reviews.db"

def create_database():
    """Creates a database to store TripAdvisor reviews."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT,
            reviewer_name TEXT,
            rating TEXT,
            review_date TEXT,
            review_text TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_review(restaurant_name, reviewer_name, rating, review_date, review_text):
    """Inserts scraped review data into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (restaurant_name, reviewer_name, rating, review_date, review_text)
        VALUES (?, ?, ?, ?, ?)
    """, (restaurant_name, reviewer_name, rating, review_date, review_text))
    conn.commit()
    conn.close()

def scrape_tripadvisor_reviews(restaurant_url, restaurant_name, num_pages=3):
    """Scrapes TripAdvisor reviews for a given restaurant."""
    
    # Set up Chrome driver
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")  # Run without opening a window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open TripAdvisor restaurant page
    driver.get(restaurant_url)
    time.sleep(5)  # Wait for page to load



    # Wait for reviews to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="REVIEWS"]/div[2]/div[2]/div[2]/div/div[1]')))

    # Find all review blocks
    reviews_section = driver.find_element(By.XPATH, '//*[@id="REVIEWS"]/div[2]/div[2]/div[2]/div/div[1]')
    reviews = reviews_section.find_elements(By.XPATH, ".//div[contains(@class, 'review-container')]")


    for review in reviews:
        try:
            reviewer_name = review.find_element(By.XPATH, ".//a[contains(@class, 'ui_header_link')]").text
        except:
            reviewer_name = "Unknown"

        try:
            rating = review.find_element(By.XPATH, ".//span[contains(@class, 'ui_bubble_rating')]").get_attribute("class")
            rating = rating.split("_")[-1]  # Extract rating number (e.g., "ui_bubble_rating bubble_50" -> "50")
            rating = str(int(rating) / 10)  # Convert to 1-5 scale
        except:
            rating = "No Rating"

        try:
            review_date = review.find_element(By.XPATH, ".//span[contains(@class, 'ratingDate')]").get_attribute("title")
        except:
            review_date = "Unknown Date"

        try:
            review_text = review.find_element(By.XPATH, ".//q[contains(@class, 'IRsGHoPm')]").text
        except:
            review_text = "No Review Text"

        # Save the review to the database
        save_review(restaurant_name, reviewer_name, rating, review_date, review_text)

    # Find and click "Next" button to go to the next page
    try:
        next_button = driver.find_element(By.XPATH, "//a[@class='ui_button nav next primary ']")
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)  # Wait for next page to load
    except:
        print("No more pages available.")
        

    # Close the browser
    driver.quit()
    print(f"Successfully scraped reviews for {restaurant_name}")

# Example usage
if __name__ == "__main__":
    create_database()
    restaurant_url = "https://www.tripadvisor.com/Restaurant_Review-g274873-d803011-Reviews-Pizzeria_FoculuS-Ljubljana_Upper_Carniola_Region.html"  # Replace with actual TripAdvisor URL
    restaurant_name = "Pizzeria FoculuS"
    scrape_tripadvisor_reviews(restaurant_url, restaurant_name, num_pages=5)

  
# //*[@id="REVIEWS"]/div[2]/div[2]/div[2]/div/div[1]