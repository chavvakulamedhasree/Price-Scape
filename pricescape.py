import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from autoscraper import AutoScraper

# Function to get the current price from the product page
def get_current_price(url):
amazon_url="https://www.amazon.in/OnePlus-Nord-Chromatic-128GB-Storage/dp/B0BY8MCQ9S/ref=sr_1_3?keywords=mobiles+under+20000&qid=1700229555&s=electronics&sr=1-3&th=1" 
 wanted_list=["19,999","OnePlus Nord CE 3 Lite 5G (Chromatic Gray, 8GB RAM, 128GB Storage)"]
    amazon_url="https://www.amazon.in/OnePlus-Nord-Chromatic-128GB-Storage/dp/B0BY8MCQ9S/ref=sr_1_3?keywords=mobiles+under+20000&qid=1700229555&s=electronics&sr=1-3&th=1"
    scraper=AutoScraper()
result=scraper.build(amazon_url,wanted_list)

    # soup = BeautifulSoup(response.text, 'html.parser')
    # # Modify this based on the HTML structure of the website you are scraping
    # price_element = soup.find('span', class_='a-price aok-align-center reinventPricePriceToPayMargin priceToPay')#, class_='product-price')
    # current_price = price_element.text.strip() if price_element else 'Not available'
    return result[0]

# Function to create or connect to the database
def create_database():


conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            price TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to track and display price history
def track_price(url):
    create_database()
    current_price = get_current_price(url)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('price_tracker.db')
    cursor = conn.cursor()

    # Insert the current price and timestamp into the database
    cursor.execute('INSERT INTO price_history (url, price, timestamp) VALUES (?, ?, ?)', (url, current_price, timestamp))
    conn.commit()
# Retrieve and display price history
    cursor.execute('SELECT * FROM price_history WHERE url=?', (url,))
    price_history = cursor.fetchall()

    print(f"Price history for {url}:\n")
    for entry in price_history:
        print(f"Timestamp: {entry[3]}, Price: {entry[2]}")

    conn.close()

# Example usage
product_url = 'https://www.amazon.in/Lava-Viridian-Dimensity-Processor-Superfast/dp/B0C467KFNM/?_encoding=UTF8&pd_rd_w=cWCIM&content-id=amzn1.sym.347be3ab-bfc6-4b7e-a51a-3c08eb930481&pf_rd_p=347be3ab-bfc6-4b7e-a51a-3c08eb930481&pf_rd_r=35HFWMKJDWR04NS3FGG7&pd_rd_wg=8iv1R&pd_rd_r=f1e9ca89-e2ef-4baa-be66-79a4e2ba605d&th=1'
track_price(product_url)
print(get_current_price(product_url)
