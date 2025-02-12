import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Database setup
DB_NAME = "google_reviews.db"

def create_database():
    """Creates a database to store Google Maps reviews."""
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

def scrape_google_reviews(restaurant_name, num_reviews=20):
    """Scrapes reviews for a given restaurant from Google Maps."""

    # Set up Chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0")  # Prevent detection
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open Google Maps
    driver.get("https://www.google.com/maps")
    time.sleep(3)  # Wait for page to load


    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for the page to scroll down
    # Handle cookie consent window
    """ try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-vQzf8d') and contains(text(), 'Accept all')]"))
        )
        accept_button.click()
        time.sleep(3)  # Wait for the consent window to close
    except:
        print("Could not find the 'Accept all' button. Continuing...")"""


    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div[3]/form[2]')))
        accept_cookies_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[3]/form[2]')
        accept_cookies_button.click()
    except Exception as e:
        print("Cookie consent dialog not found or already handled.", e)

    # Wait for the page to load
    time.sleep(2)


    # Search for the restaurant
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='searchboxinput']"))
    )
    search_box.send_keys(restaurant_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for results to load

    # Click the first result (if necessary)
    try:
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/maps/place/') and contains(@class, 'hfpxzc')]"))
        )
        first_result.click()
        time.sleep(5)  # Wait for restaurant page to load
    except:
        print("Could not click the first result. Continuing...")

    """# Scroll down to reviews
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)"""

    # Click on "More Reviews"
    try:
        more_reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Reviews')]"))
        )
        more_reviews_button.click()
        time.sleep(5)  # Wait for reviews to load
    except:
        print("Could not find 'More Reviews' button. Exiting...")
        driver.quit()
        return

    # Scroll through reviews (simulate user scrolling)
    scrollable_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'm6QErb')]"))
    )

    for _ in range(10):  # Adjust scroll count as needed
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)  # Allow time for more reviews to load

    # Extract review elements
    reviews = driver.find_elements(By.XPATH, "//div[contains(@class, 'jftiEf')]")[:num_reviews]

    for review in reviews:
        try:
            reviewer_name = review.find_element(By.XPATH, ".//div[contains(@class, 'd4r55')]").text
        except:
            reviewer_name = "Unknown"

        try:
            rating_element = review.find_element(By.XPATH, ".//span[contains(@class, 'kvMYJc')]")
            rating = rating_element.get_attribute("aria-label").split(" ")[0]  # Extract rating (e.g., "5.0 out of 5")
        except:
            rating = "No Rating"

        try:
            review_date = review.find_element(By.XPATH, ".//span[contains(@class, 'rsqaWe')]").text
        except:
            review_date = "Unknown Date"

        try:
            review_text = review.find_element(By.XPATH, ".//span[contains(@class, 'wiI7pd')]").text
        except:
            review_text = "No Review Text"

        # Save the review to the database
        save_review(restaurant_name, reviewer_name, rating, review_date, review_text)

    # Close the browser
    driver.quit()
    print(f"Successfully scraped {len(reviews)} reviews for {restaurant_name}")

def read_restaurant_list(file_path):
    """Reads a list of restaurant names from a file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Example usage
if __name__ == "__main__":
    create_database()
    restaurant_list = read_restaurant_list('restaurants.txt')
    for restaurant_name in restaurant_list:
        scrape_google_reviews(restaurant_name, num_reviews=20)
        time.sleep(10)  # Delay between consequtive scrapes to avoid detection
