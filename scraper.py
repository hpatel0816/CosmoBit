import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

NATURE_BASE_URL = "https://www.nature.com/subjects/"
CATEGORIES = ["astronomy-and-planetary-science"]
#CATEGORIES = ["astronomy-and-planetary-science", "space-physics"]

def scrape_category(category):
    url = f"{NATURE_BASE_URL}{category}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for category: {category}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    #print(articles)

    data = []
    for article in articles:
        title = article.find('h3').text.strip()
        
        authors_tag = article.find('ul', {'class': 'c-author-list'})
        if authors_tag:
            authors = ', '.join([li.text.strip() for li in authors_tag.find_all('li')])
        else:
            authors = 'No authors listed'

        link_tag = article.find('a', href=True)
        link = 'https://www.nature.com' + link_tag['href'] if link_tag else 'No link available'

        # Check if the article is Open Access
        open_access_tag = article.find('span', itemprop='openAccess')
        is_open_access = open_access_tag is not None

        data.append({
            'Title': title,
            'Authors': authors,
            'Link': link,
            'OpenAccess': is_open_access
        })

    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)

    # Save the DataFrame to a JSON file in the data folder
    json_filename = f"nature_{category.replace('-', '_')}.json"
    #json_path = os.path.join('../data/categories/', json_filename)

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {json_filename}")



for category in CATEGORIES:
    print(f"Scraping category: {category}")
    scrape_category(category)