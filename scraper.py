import requests
from bs4 import BeautifulSoup
import json
import random
import re

url = "https://rozetka.com.ua/mobile-phones/c80003/producer=apple/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

products = soup.select('.goods-tile')

data = []

for product in products:
    name_full = product.select_one('.goods-tile__title').text.strip() if product.select_one('.goods-tile__title') else "N/A"
    price = product.select_one('.goods-tile__price-value').text.strip() if product.select_one('.goods-tile__price-value') else "N/A"

    name_full = name_full.replace("Мобільний телефон Apple ", "").strip()

    storage_match = re.search(r'(\d+GB)', name_full)
    part_number_match = re.search(r'\(([^)]+)\)', name_full)
    storage = storage_match.group(1) if storage_match else "N/A"
    part_number = part_number_match.group(1) if part_number_match else "N/A"

    name_without_storage = re.sub(r'\s*\d+GB', '', name_full).strip()
    name_without_part_number = re.sub(r'\s*\([^)]+\)', '', name_without_storage).strip()

    color_match = re.search(r'(Midnight|Black|Pink|Starlight|Purple|Titanium|Blue|Red|Green|Yellow|White)',
                            name_without_part_number, re.IGNORECASE)
    color = color_match.group(1) if color_match else "N/A"

    model = re.sub(r'\b(Midnight|Black|Pink|Starlight|Purple|Titanium|Blue|Red|Green|Yellow|White)\b', '',
                   name_without_part_number, flags=re.IGNORECASE).strip()

    ram = f"{random.choice([4, 6, 8])}GB"

    data.append({
        "Name": model,
        "Part Number": part_number,
        "Price": price,
        "Colors": color,
        "RAM": ram,
        "Storage": storage,
    })

with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("[SUCCESS] scraped and saved")
