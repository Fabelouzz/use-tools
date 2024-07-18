import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_cheapest_option(input_str):
    """
    Find the cheapest MacBook Air 13 on the PriceRunner website.

    Parameters:
    input_str (str): A JSON string representing a dictionary with a single key 'product_name'.
                     Example: '{"product_name": "macbook air 13"}'

    Returns:
    str: The formatted result of the cheapest MacBook Air 13 found on the PriceRunner website.

    Raises:
    Exception: If an error occurs during the web scraping process.
    """
    try:
        # Parse the input string
        input_dict = json.loads(input_str)
        product_name = input_dict['product_name']
    except (json.JSONDecodeError, KeyError) as e:
        return str(e), "Invalid input format. Please provide a valid JSON string."

    # Construct the search URL
    base_url = 'https://www.pricerunner.se/results?q='
    search_url = base_url + product_name.replace(' ', '%20')
    site_url = 'https://www.pricerunner.se'
    
    # Set up Selenium WebDriver with the full path to chromedriver.exe
    service = Service(executable_path=r'C:\Users\Kunge\chromedrivers\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    
    try:
        # Open the search URL directly
        driver.get(search_url)
        
        # Wait for the cookies consent window and accept it
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Acceptera"]'))
            )
            consent_button.click()
        except Exception as e:
            print("Cookies consent window did not appear or could not be interacted with:", e)
        
        # Wait for search results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pr-gkzc8z-Carousel-scrollSnapChild'))
        )
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the product containers
        product_list = soup.find_all('div', class_='pr-gkzc8z-Carousel-scrollSnapChild')
        
        if not product_list:
            return "No products found."

        cheapest_option = None
        lowest_price = float('inf')
        
        for product in product_list:
            try:
                # Extract the name and price
                name_tag = product.find('h3', class_='pr-kxc9l9')
                price_tag = product.find('span', class_='pr-2v77sd', attrs={'data-testid': 'priceComponent'})

                if name_tag and price_tag:
                    name = name_tag['title'].strip()
                    price_str = price_tag.text.strip().replace('\xa0', ' ')  # Replace non-breaking spaces
                    price_str = price_str.replace('kr', '').replace(' ', '').replace(',', '.')
                    
                    price = float(price_str)
                    
                    if price < lowest_price:
                        lowest_price = price
                        cheapest_option = {
                            'name': name,
                            'price': price,
                            'link': site_url + product.find('a')['href']
                        }
            except (AttributeError, ValueError) as e:
                print(f"Error processing product entry: {e}")
                continue
        
        if cheapest_option:
            result_formatted = (
                f"\n\nCheapest Option:\n"
                f"Name: {cheapest_option['name']}\n"
                f"Price: {cheapest_option['price']} kr\n"
                f"Link: {cheapest_option['link']}\n"
                f"Fetched using get_cheapest_option."
            )
            return result_formatted
        else:
            return "No products found."
    
    finally:
        # Close the WebDriver after a short delay to ensure all actions are completed
        time.sleep(5)
        driver.quit()
