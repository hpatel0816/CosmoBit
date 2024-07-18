import requests
from bs4 import BeautifulSoup

class CategoryScraper:
    def __init__(self):
        self.soup = None

    def fetch_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            print(f"Failed to retrieve data from URL: {url}")
            self.soup = None

    def extract_articles(self):
        if not self.soup:
            return []
        articles = self.soup.find_all('article')
        data = []
        for article in articles:
            # Extract the article title and authors
            title = article.find('h3').text.strip()
            authors_tag = article.find('ul', {'class': 'c-author-list'})
            authors = ', '.join([li.text.strip() for li in authors_tag.find_all('li')]) if authors_tag else 'No authors listed'

            # Extract the link to article
            link_tag = article.find('a', href=True)
            link = 'https://www.nature.com' + link_tag['href'] if link_tag else 'No link available'

            # Extract article type
            type_tag = article.find('span', class_='c-meta__type')
            article_type = type_tag.text.strip() if type_tag else 'Unknown'

            # Extract publish date
            date_tag = article.find('time', itemprop='datePublished')
            publish_date = date_tag['datetime'] if date_tag else 'Unknown'

            # Check if the article is of Open Access type
            open_access_tag = article.find('span', itemprop='openAccess')
            is_open_access = open_access_tag is not None

            data.append({
                'Title': title,
                'Type': article_type,
                'OpenAccess': is_open_access,
                'PublishDate': publish_date,
                'Authors': authors,
                'Link': link,
            })
        return data

    def scrape_category(self, url):
        self.fetch_page(url)
        return self.extract_articles()