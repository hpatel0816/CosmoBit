import requests
from bs4 import BeautifulSoup
import logging

class ArticleScraper:
    def __init__(self):
        self.soup = None

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.content, 'html.parser')
            else:
                logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                self.soup = None
        except Exception as e:
            logging.error(f"Exception in fetch_page: {e}")

    def extract_title(self):
        try:
            title_tag = self.soup.find('h1', class_=['c-article-title', 'c-article-magazine-title'])
            return title_tag.text.strip() if title_tag else None
        except Exception as e:
            logging.error(f"Exception in extract_title: {e}")
            return None

    def extract_authors(self):
        try:
            if not self.soup:
                return []
            author_list = self.soup.find('ul', class_='c-article-author-list')
            return [author.text.strip() for author in author_list.find_all('li')] if author_list else []
        except Exception as e:
            logging.error(f"Exception in extract_authors: {e}")
            return []

    def extract_related_articles(self, is_open_access):
        try:
            if not self.soup and not is_open_access:
                return []
            related_articles_section = self.soup.find('div', class_='c-article-recommendations-list')
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
            return related_articles
        except Exception as e:
            logging.error(f"Exception in extract_related_articles: {e}")
            return []

    def extract_sections(self, is_open_access):
        try:
            if not self.soup:
                return {'abstract': '', 'intro': '', 'results': ''}

            if is_open_access:
                sections_to_extract = {
                    'abstract': 'abstract',
                    'intro': ['main', 'introduction'],
                    'results': ['findings', 'results', 'conclusion', 'summary']
                }
                sections = {'abstract': '', 'intro': '', 'results': ''}

                abstract_section = self.soup.find('section', {'data-title': 'Abstract'})
                sections['abstract'] = abstract_section.find('p').text.strip() if abstract_section else 'Abstract not found.'

                main_content_section = self.soup.find('div', class_='main-content')
                if main_content_section:
                    for section in main_content_section.find_all('section'):
                        section_title = section.get('data-title', '').lower()
                        section_text = section.get_text(separator='\n').strip()
                        if any(keyword in section_title for keyword in sections_to_extract['intro']):
                            sections['intro'] = section_text
                        elif any(keyword in section_title for keyword in sections_to_extract['results']):
                            sections['results'] = section_text
            else:
                sections = {'highlights': ''}
                teaser_section = self.soup.find('div', class_='article__teaser')
                if teaser_section:
                    sections['highlights'] = '\n'.join([p.text.strip() for p in teaser_section.find_all('p')])

            return sections
        except Exception as e:
            logging.error(f"Exception in extract_sections: {e}")
            return {'abstract': '', 'intro': '', 'results': ''}

    def extract_figures(self, is_open_access):
        try:
            if not self.soup or not is_open_access:
                return {}
            figures = {}
            figure_elements = self.soup.find_all('figure')
            base_url = 'https://www.nature.com'
            for figure in figure_elements:
                fig_caption_tag = figure.find('b', class_='c-article-section__figure-caption')
                if fig_caption_tag:
                    fig_id = fig_caption_tag.get('id')
                    fig_caption = fig_caption_tag.text.strip()
                    fig_link_tag = figure.find('a', class_='c-article-section__figure-link')
                    fig_link = base_url + fig_link_tag['href'] if fig_link_tag else None
                    figures[fig_id] = {
                        'caption': fig_caption,
                        'link': fig_link
                    }
            return figures
        except Exception as e:
            logging.error(f"Exception in extract_figures: {e}")
            return {}

    def scrape_article(self, url, is_open_access):
        try:
            self.fetch_page(url)
            if not self.soup:
                return None
            article_data = {
                'title': self.extract_title(),
                'authors': self.extract_authors(),
                'related_articles': self.extract_related_articles(is_open_access),
                'content': self.extract_sections(is_open_access),
                'figures': self.extract_figures(is_open_access),
                'OpenAccess': is_open_access
            }
            return article_data
        except Exception as e:
            logging.error(f"Exception in scrape_article: {e}")
            return None