from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from collections import Counter

# Function to check the date
def get_date():
    # A mapping of English month names to Slovenian
    english_to_slovenian_months = {
        'January': 'januar',
        'February': 'februar',
        'March': 'marec',
        'April': 'april',
        'May': 'maj',
        'June': 'junij',
        'July': 'julij',
        'August': 'avgust',
        'September': 'september',
        'October': 'oktober',
        'November': 'november',
        'December': 'december'
    }

    # A mapping of English day names to Slovenian
    english_to_slovenian_days = {
        'Monday': 'ponedeljek',
        'Tuesday': 'torek',
        'Wednesday': 'sreda',
        'Thursday': 'četrtek',
        'Friday': 'petek',
        'Saturday': 'sobota',
        'Sunday': 'nedelja'
    }

    # Get the current date
    current_date = datetime.now()

    # Get the Slovenian month name from the mapping
    slovenian_month = english_to_slovenian_months[current_date.strftime("%B")]

    # Get the Slovenian day name from the mapping
    slovenian_day = english_to_slovenian_days[current_date.strftime("%A")]

    # Format the current date as a Slovenian date string
    slovenian_date_string = f"{slovenian_day}, {current_date.day}. {slovenian_month}"

    current_date = slovenian_date_string

    time_now = datetime.now()
    time_h = int(time_now.strftime("%H"))
    time_m = int(time_now.strftime("%M"))
    current_time = time_h + time_m/100
    
    return current_date, current_time

# Function for getting menu
def get_meni(current_day):

    #firefox_options = webdriver.FirefoxOptions()
    #firefox_options.headless = True  # Run in headless mode
    #firefox_options.add_argument("--headless")

    # Initialize the Firefox WebDriver with the options
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open Google Maps
    driver.get("https://fe.uni-lj.si/o-fakulteti/restavracija/")

    # Wait for the cookie consent dialog to be visible and accept it
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div/div/button[2]')))
        accept_cookies_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div/button[2]')
        accept_cookies_button.click()
    except Exception as e:
        output_text = "Žal je prišlo do težave s spletno stranjo. Hvala za razumevanje, naslednjič se bom bolj potrudil."
        #print("Cookie consent dialog not found or already handled.", e)
        # Close the browser
        driver.quit()
        return output_text

    # Wait for the page to load
    time.sleep(2)
    try:
        dan1 = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[1]/h2/button/strong').text
    except Exception as e:
        #print("Meni za dan 1 not found.", e)
        dan1 = "NaN"
    try:
        dan2 = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/h2/button/strong').text
    except Exception as e:
        #print("Meni za dan 2 not found.", e)
        dan2 = "NaN"
    try:
        dan3 = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div[1]/h2/button/strong').text
    except Exception as e:
        #print("Meni za dan 3 not found.", e)
        dan3 = "NaN"
    try:
        dan4 = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[4]/div[1]/h2/button/strong').text
    except Exception as e:
        #print("Meni za dan 4 not found.", e)
        dan4 = "NaN"
    try:
        dan5 = driver.find_element(By.XPATH, '/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[5]/div[1]/h2/button/strong').text
    except Exception as e:
        #print("Meni za dan 5 not found.", e)
        dan5 = "NaN"

    if current_day == dan1:
        i = 1
    elif current_day == dan2:
        i = 2
    elif current_day == dan3:
        i = 3
    elif current_day == dan4:
        i = 4
    elif current_day == dan5:
        i = 5
    else:
        i = 999
        error_text = 'Dons je vikend butl kaj delas na faksu!'

    try:
        li1 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[1]')
        me1 = True
    except Exception as e:
        #print("Meni 1 not found.", e)
        me1 = False
    try:
        li2 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[2]')
        me2 = True
    except Exception as e:
        #print("Meni 2 not found.", e)
        me2 = False
    try:
        li3 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[3]')
        me3 = True
    except Exception as e:
        #print("Meni 3 not found.", e)
        me3 = False
    try:
        li4 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[4]')
        me4 = True
    except Exception as e:
        #print("Meni 4 not found.", e)
        me4 = False
    try:
        li5 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[5]')
        me5 = True
    except Exception as e:
        #print("Meni 5 not found.", e)
        me5 = False
    try:
        li6 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[6]')
        me6 = True
    except Exception as e:
        #print("Meni 6 not found.", e)
        me6 = False
    try:
        li7 = driver.find_element(By.XPATH, f'/html/body/main/div/section[2]/div/div/div/div[2]/div/div[1]/div[2]/div[{i}]/div[2]/div/ul/li[7]')
        me7 = True 
    except Exception as e:
        #print("Meni 7 not found.", e)
        me7 = False

    script = """
    var li = arguments[0];
    var textContent = li.textContent || li.innerText;
    return textContent.trim();
    """
    output = []
    
    if i == 999:
        output = error_text
    else:
        if me1 == True:
            meni1 = driver.execute_script(script, li1)
            output.append(meni1)

        if me2 == True:
            meni2 = driver.execute_script(script, li2)
            output.append(meni2)

        if me3 == True:
            meni3 = driver.execute_script(script, li3)
            output.append(meni3)

        if me4 == True:
            meni4 = driver.execute_script(script, li4)
            output.append(meni4)

        if me5 == True:
            meni5 = driver.execute_script(script, li5)
            output.append(meni5)

        if me6 == True:
            meni6 = driver.execute_script(script, li6)
            output.append(meni6)

        if me7 == True:
            meni7 = driver.execute_script(script, li7)
            output.append(meni7)
    
    # Close the browser
    driver.quit()

    return output

def preprocess_strings(strings, placeholder="COMMAPLACEHOLDER"):
    # Replace commas with a placeholder and ensure spaces around placeholders
    temp_strings = [s.replace(',', ' ' + placeholder + ' ') for s in strings]
    
    # Remove everything to the left of the colon, including the colon itself
    # If a colon is present, keep the part after the colon; otherwise, keep the whole string
    temp_strings = [s.split(':', 1)[-1] if ':' in s else (s.split(')', 1)[-1] if ')' in s else s) for s in temp_strings]

    # Remove periods
    remove_punct = str.maketrans('', '', '.')
    cleaned_strings = [s.translate(remove_punct) for s in temp_strings]
    return cleaned_strings

def find_common_words_in_first_three(strings, placeholder="COMMAPLACEHOLDER"):
    # Only consider the first three strings
    first_three_strings = strings[:3]
    # Clean up periods and split each string into a set of words
    word_sets = [set(s.replace('.', '').split()) for s in first_three_strings]
    # Find the intersection of these sets
    common_words = set.intersection(*word_sets)
    return common_words, placeholder

def remove_common_words_from_all(strings, common_words, placeholder):
    # Remove common words from all strings
    updated_strings = []
    for s in strings:
        words = s.split()
        filtered_words = [word for word in words if word.replace(placeholder, '').replace('.', '') not in common_words]
        updated_string = ' '.join(filtered_words)
        updated_strings.append(updated_string)
    return updated_strings

def postprocess_strings(strings, placeholder="COMMAPLACEHOLDER"):
    # Step 1: Preprocess strings to replace commas with a placeholder
    preprocessed_strings = preprocess_strings(strings)
    # Step 2: Find common words in the first three preprocessed strings
    common_words, placeholder = find_common_words_in_first_three(preprocessed_strings)
    # Step 3: Remove common words from all preprocessed strings
    updated_preprocessed_strings = remove_common_words_from_all(preprocessed_strings, common_words, placeholder)

    # Replace placeholders back to commas and remove trailing commas if present
    final_strings = [s.replace(placeholder, ',').rstrip(',').replace(" , ", ", ").lstrip(', ').replace("s tuno ali piščancem,", "solata s tuno ali piščancem,") for s in updated_preprocessed_strings]
    return final_strings

# Function for getting soup and salad
def process_soup_salad(txt):
    soups = []
    salads =[]
    # Split the string on ":" and strip spaces
    for i in range(0, len(txt)):
        try:
        # _, food_temp = [item.strip() for item in txt.split(":")]
            delimiter = ":" if ":" in txt[i] else ")"
            _, food_temp = [item.strip() for item in txt[i].split(delimiter)]
        except Exception as e:
            #print(e)
            soups.append("Spet so narobe meni napisal.")
            salads.append("Ne men težit, če ne dela.")
            return soups, salads

        # Split the food on "," to separate the soup, salad and main course
        food = [item.strip() for item in food_temp.split(",")]
    
        soups.append(food[0])
        salads.append(food[-1])

    return soups, salads

# Get the most frequent soup and salad
def final_soup_salad(strings):
    # Count the frequency of each string
    string_counts = Counter(strings)
    # Find the string with the highest frequency
    most_common_string = string_counts.most_common(1)[0][0]

    return most_common_string

# Function for getting menus
def process_menu(txt):
    menu = []
    # Split the string on ":" or ")" to get menu 1, menu 2,...
    for i in range(0,len(txt)):
        try:
            #menu_temp, _ = [item.strip() for item in txt[i].split(":")]
            delimiter = ":" if ":" in txt[i] else ")"
            menu_temp, _ = [item.strip() for item in txt[i].split(delimiter)]
        except Exception as e:
            #print(e)
            menu = "Spet so narobe napisal meni. Ne men težit, če ne dela."
            return menu

        # Append all menus in a list
        menu.append(menu_temp)

    return menu

# Function for generating text string
def generate_text():
    gen_text = []
    output_text = ""
    # Call function get_date()
    date, time = get_date()

    if date.split(", ")[0] == "nedelja" or date.split(", ")[0] == "sobota":
        gen_text = 'Dons je vikend butl kaj delaš na faksu!'
        gen_text_temp = [char for char in gen_text]
        output_text = '\n'.join(gen_text[i] for i in range(len(gen_text_temp)))
    else:
        if time < 14.30:
            # Call function get_meni()
            gen_text = get_meni(date)
            main_dish = postprocess_strings(gen_text)
            menus = process_menu(gen_text)
            # Generate a modified text string
            soups, salads = process_soup_salad(gen_text)
            soup = final_soup_salad(soups)
            salad = final_soup_salad(salads)
            if time < 9.59:
                output_text = "A smo že lačni kolega? Bo treba najprej zajtrk jest." + '\n' + '\n' + "Menza_FE: " +  date + '\n' + soup + '\n' + salad + '\n'
            else:
                output_text = "Menza_FE: " +  date + '\n' + soup + '\n' + salad + '\n'

            for i in range(0,len(main_dish)):
                output_text = output_text + menus[i] + ": " + main_dish[i] + '\n'

            # Remove the last '\n'
            if output_text.endswith('\n'):
                output_text = output_text[:-1]
        else:
            gen_text = "Jooooj kolega FE_menza je že zaprta. Bo treba u MEKA!"
            gen_text_temp = [char for char in gen_text]
            output_text = '\n'.join(gen_text[i] for i in range(len(gen_text_temp)))

    return output_text

last_scrape_date = None
text = ""

def main_menza():
    global last_scrape_date, text

    today = get_date()

    if last_scrape_date == today and text.split('\n', 1)[0]:
        #print(text)
        return text
    else:
        # Update the global variables with new scrape information
        text = generate_text()
        last_scrape_date = today
        #print(text)
        return text

test = main_menza()