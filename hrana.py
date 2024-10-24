from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import random

# Function to check the date
def get_date():
    # Get current date
    date_now = datetime.now()
    current_date = date_now.strftime('%d-%m-%Y')

    # Get current time
    time_now = datetime.now()
    time_h = int(time_now.strftime("%H"))
    time_m = int(time_now.strftime("%M"))
    current_time = time_h + time_m/100
    
    return current_date, current_time

# Function for getting menu
def restaurant_menu(restaurant_name):
    dodatek = ""
    meni = ""
    date = ""
    random_restaurant_name = ""
    num_restaurants = []
    working_hours = []
    output_text = []
    critical_error = 0

    # Initialize the Firefox WebDriver with the options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open Google Maps
    driver.get("https://www.studentska-prehrana.si/sl/restaurant")

    # Wait for the cookie consent dialog to be visible and accept it
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div/div/div/div/div[2]/div/p/a')))
        accept_cookies_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[4]/div/div/div/div/div[2]/div/p/a')
        accept_cookies_button.click()
    except Exception as e:
        critical_error = 1
        #print("Cookie consent dialog not found or already handled.", e)
        output_text = "Nism js kriv. To so neki spleno stran dol vrgl."
            
        # Close the browser
        driver.quit()
        return output_text, date, working_hours, critical_error

    # Wait for the page to load
    time.sleep(2)

    # Suggest random restaurant
    if restaurant_name == "random":
        # Generate a random number between 1 and 321 
        random_restaurant = random.randint(1, 321)
        random_restaurant_str = str(random_restaurant)
        try:
            random_restaurant_name = driver.find_element(By.XPATH, f"/html/body/div[3]/div[3]/div/div[7]/div[{random_restaurant_str}]/div/div/div/div[1]/div/div[1]/h2/a").text
            critical_error = 3
            output_text = "Random restavracija samo zate: " + random_restaurant_name

            # Close the browser
            driver.quit()
            return output_text, date, working_hours, critical_error
        except Exception as e:
            critical_error = 1
            output_text = "Kolega ne da se mi zdele iskat random restavracije sam zate, kr sam si zber neki."

            # Close the browser
            driver.quit()
            return output_text, date, working_hours, critical_error

    # Find search bar and enter desired restaurant name
    try:
        search = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[3]/form/section/label/input')
        search.click()
        search.send_keys(restaurant_name)
        search.send_keys(Keys.RETURN)
    except Exception as e:
        critical_error = 1
        #print("Search bar not found.", e)
        output_text = "Nism js kriv. To so neki spleno stran dol vrgl."
            
        # Close the browser
        driver.quit()
        return output_text, date, working_hours, critical_error

    # Wait for the page to load
    time.sleep(2)

    # Translate upper, lower case for searching restaurants
    xpath = f"//h2/a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{restaurant_name.lower()}')]"

    # Find how many restaurants matches the input
    try:
        num_restaurants_temp = driver.find_elements(By.XPATH, xpath)
        #num_restaurants_temp = driver.find_elements(By.XPATH, f"/html/body/div[3]/div[3]/div/div[7]//div/div/div/div/div/div/h2/a[contains(text(), {restaurant_name})]")
        for element in num_restaurants_temp:
            num_restaurants.append(element.text)
        num_restaurants = [element for element in num_restaurants if element != ''] 
    except Exception as e:
        num_restaurants = []
        #print("Error", e)

    # If only one restaurant matches the name, return the menu
    if len(num_restaurants) == 1:
        restaurant_name = num_restaurants[0]
    # If more than one restaurant matches the name return list of restaurants
    elif len(num_restaurants) > 1:
        critical_error = 2
        output_text = num_restaurants
        # Close the browser
        driver.quit()
        return output_text, date, working_hours, critical_error

    # Select the restaurant
    try:
        restaurant = driver.find_element(By.LINK_TEXT, restaurant_name)
        restaurant.click()
    except Exception as e:
        critical_error = 1
        #print("Restaurant not found.", e)
        output_text = "Ej sori ne najdem restavracije. Al si narobe ime napisou al so jo pa zaprl. Nism js kriv."
            
        # Close the browser
        driver.quit()
        return output_text, date, working_hours, critical_error

    time.sleep(2)

    # Get current date
    try:
        current_date = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div[2]/div/div/div[1]/div/div[1]/a[1]').text
        date = current_date
    except Exception as e:
        #print("Date not found.", e)
        date = ""

    # Get working hours
    try:
        working_hours = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div[2]/div/div/div[1]/div/div[1]/div[3]/div/div[2]/div').text
        working_hours = [element for element in working_hours if element not in [' ', '\n']]
    except Exception as e:
        #print("Meni i not found.", e)
        working_hours = [""]

    # Get the extras from the page
    for j in range(1, 5):
        if dodatek != "NaN":
            try:
                dodatek = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/ul/li[{j}]/i').text
                output_text.append(dodatek)
            except Exception as e:
                dodatek = "NaN"
    
    # Get the menus from the page
    for i in range(1, 40):
        if meni != "NaN":
            try:
                meni = driver.find_element(By.XPATH, f'/html/body/div[3]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[{i}]/div/div/div[1]/h5/strong').text
                output_text.append(meni)
            except Exception as e:
                meni = "NaN"
                #print(f"Meni {i} not found.", e)
    
    # Close the browser
    driver.quit()

    return output_text, date, working_hours, critical_error

# Function for generating text string
def generate_text(restaurant):
    gen_text = []
    output_text = ""

    # Call function restaurant_menu()
    gen_text_temp, date, working_hours, critical_error = restaurant_menu(restaurant)
    if critical_error == 1:
        output_text = ''.join(gen_text_temp)
    elif critical_error == 2:
        output_text = "Našel sem naslednje restavracije, prosim izberite eno in ponovite iskanje: " + '\n' + '\n'.join(gen_text_temp[i] for i in range(len(gen_text_temp)))
    elif critical_error == 3:
        output_text = ''.join(gen_text_temp[i] for i in range(len(gen_text_temp)))
    else:
        gen_text = [string.lower() for string in gen_text_temp]
        working_hours_joined = ''.join(working_hours)
        final_working_hours = working_hours_joined.replace('Medtednom', 'Med tednom').replace('Sobota', '\nSobota').replace('Nedelja', '\nNedelja')
        output_text = "Meni za restavracijo: " + restaurant + ", " + date + '\n' + '\n' + final_working_hours + '\n' + '\n' + '\n'.join(gen_text[i] for i in range(len(gen_text)))

    return output_text

def load_puns_facts(filename):
    """Load puns from a text file into a list."""
    with open(filename, 'r') as file:
        puns_facts = file.read().splitlines()
    return puns_facts

def get_random_pun_fact(filename):
    """Select and return a random pun from the list."""
    puns_facts = load_puns_facts(filename)  # Load puns from file
    return random.choice(puns_facts)  # Select a random pun

puns_file = './files/food_puns.txt'
facts_file = './files/food_facts.txt'

def main_restaurant(restaurant):
    if restaurant == "pun":
        try:
            random_pun = get_random_pun_fact(puns_file)
        except Exception as e:
            random_pun = "Searching for a pun? Today's forecast looks pretty 'pun-ny' with a high chance of groans, but alas, we're experiencing an unexpected pun drought!"
        return random_pun
    elif restaurant == "fact":
        try:
            random_fact = get_random_pun_fact(facts_file)
        except Exception as e:
            random_fact = "Did you know? The most elusive ingredient in the culinary world isn’t truffle or saffron, but the random food fact you’re craving right now. It's rumored to vanish into the pantry of forgotten flavors, only to reappear when you're searching for a different seasoning."
        return random_fact
    else:
        text = generate_text(restaurant)
        return text

# restaurant = "random"
# a=main_restaurant(restaurant)
# print(a)