import requests
from bs4 import BeautifulSoup
import json

# URL of the research paper
url = 'https://www.nature.com/articles/s41467-024-49237-6'  # URL of the research paper

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.content
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract article title
title = soup.find('h1', class_='c-article-title').text.strip()

# Extract authors
author_list = soup.find('ul', class_='c-article-author-list')
authors = [author.text.strip() for author in author_list.find_all('li')]

# Extract related articles
related_articles_section = soup.find('div', class_='c-article-recommendations-list')
related_articles = []
if related_articles_section:
    for item in related_articles_section.find_all('div', class_='c-article-recommendations-list__item'):
        article = item.find('article', class_='c-article-recommendations-card')
        article_image = article.find('img')['src']
        article_title = article.find('h3', class_='c-article-recommendations-card__heading').find('a').text.strip()
        article_link = article.find('a')['href']
        article_publish_date = article.find('span', class_='c-article-meta-recommendations__date').text.strip()
        related_articles.append({
            'image': article_image,
            'title': article_title,
            'publish_date': article_publish_date,
            'link': article_link
        })


# Extract main content
main_content_section = soup.find('div', class_='main-content')

sections_to_extract = {
    'abstract': 'abstract',
    'intro': ['main', 'introduction'],
    'results': ['findings', 'results', 'conclusion']
}

sections = {'abstract': '', 'intro': '', 'results': ''}

# Extract abstract section
abstract_section = soup.find('section', {'data-title': 'Abstract'})
sections['abstract'] = abstract_section.find('p').text.strip() if abstract_section else 'Abstract not found.'

if main_content_section:
    for section in main_content_section.find_all('section'):
        section_title = section.get('data-title', '').lower()
        section_text = section.get_text(separator='\n').strip()
        
        if any(keyword in section_title for keyword in sections_to_extract['intro']):
            sections['intro'] = section_text
        elif any(keyword in section_title for keyword in sections_to_extract['results']):
            sections['results'] = section_text


# Extract figures and their details
figures = {}
figure_elements = soup.find_all('figure')
base_url = 'https://www.nature.com'

for figure in figure_elements:
    fig_id = figure.find('b', class_='c-article-section__figure-caption').get('id')
    fig_caption = figure.find('b', class_='c-article-section__figure-caption').text.strip()
    fig_link = base_url + figure.find('a', class_='c-article-section__figure-link')['href']
    figures[fig_id] = {
        'caption': fig_caption,
        'link': fig_link
    }

# Organize data in a dictionary
article_data = {
    'title': title,
    'authors': authors,
    'related_articles': related_articles,
    'content': {
        'abstract': sections['abstract'],
        'intro': sections['intro'],
        'results': sections['results'],
    },
    'figures': figures
}

# Save to JSON file
with open('../data/articles/article_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(article_data, json_file, ensure_ascii=False, indent=4)


print("Article data has been saved to article_data.json")
