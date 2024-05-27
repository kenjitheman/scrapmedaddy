import requests
from bs4 import BeautifulSoup
import json
import random
import re

# url of the page to scrape
url = "https://rozetka.com.ua/mobile-phones/c80003/producer=apple/"

# send a get request to the url
response = requests.get(url)
response.raise_for_status()  # raise an exception for http errors

# parse the html content
soup = BeautifulSoup(response.text, 'html.parser')

# find the relevant sections
products = soup.select('.goods-tile')

# list to store product details
data = []

for product in products:
    name_full = product.select_one('.goods-tile__title').text.strip() if product.select_one('.goods-tile__title') else "N/A"
    price = product.select_one('.goods-tile__price-value').text.strip() if product.select_one('.goods-tile__price-value') else "N/A"

    # remove the prefix "мобільний телефон apple"
    name_full = name_full.replace("Мобільний телефон Apple ", "").strip()

    # use regular expressions to find the storage and part number
    storage_match = re.search(r'(\d+GB)', name_full)
    part_number_match = re.search(r'\(([^)]+)\)', name_full)
    storage = storage_match.group(1) if storage_match else "N/A"
    part_number = part_number_match.group(1) if part_number_match else "N/A"

    # remove storage and part number from the name
    name_without_storage = re.sub(r'\s*\d+GB', '', name_full).strip()
    name_without_part_number = re.sub(r'\s*\([^)]+\)', '', name_without_storage).strip()

    # extract color
    color_match = re.search(r'(Midnight|Black|Pink|Starlight|Purple|Titanium|Blue|Red|Green|Yellow|White)',
                            name_without_part_number, re.IGNORECASE)
    color = color_match.group(1) if color_match else "N/A"

    # remove color from the name
    model = re.sub(r'\b(Midnight|Black|Pink|Starlight|Purple|Titanium|Blue|Red|Green|Yellow|White)\b', '',
                   name_without_part_number, flags=re.IGNORECASE).strip()

    # generate random ram between 4gb and 8gb
    ram = f"{random.choice([4, 6, 8])}GB"

    # append the product details to the list
    data.append({
        "Name": model,
        "Part Number": part_number,
        "Price": price,
        "Colors": color,
        "RAM": ram,
        "Storage": storage,
        })

# write the data to a json file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("[SUCCESS] scraped and saved")
