import json
import time
import logging

from web_scraper.category_scraper import CategoryScraper
from web_scraper.article_scraper import ArticleScraper

NATURE_BASE_URL = "https://www.nature.com/subjects/"
CATEGORIES = ["astronomy-and-planetary-science", "space-physics"]

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    category_scraper = CategoryScraper()
    article_scraper = ArticleScraper()

    for category in CATEGORIES:
        try:
            logging.info(f"Scraping category: {category}")
            articles = category_scraper.scrape_category(f"{NATURE_BASE_URL}{category}")

            if articles:
                json_file_path = f"nature_{category.replace('-', '_')}.json"
                save_to_json(articles, json_file_path)
                logging.info(f"Category data saved to {json_file_path}")

                for article in articles:
                    try:
                        article_url = article['Link']
                        is_open_access = article['OpenAccess']
                        logging.info(f"Scraping article: {article_url}")
                        article_data = article_scraper.scrape_article(article_url, is_open_access)
                        if article_data:
                            article_id = article_url.split('/')[-1]
                            article_json_path = f"article_{article_id}_data.json"
                            save_to_json(article_data, article_json_path)
                            logging.info(f"Article data saved to {article_json_path}")
                            # Wait 1.5 seconds before scraping the next article
                        time.sleep(1)
                    except Exception as e:
                        logging.error(f"Failed to scrape the {article} article. Error: {e}")
            # Wait 5 seconds before scraping the next category
            time.sleep(5)
        except Exception as e:
            logging.error(f"Failed to scrape the {category} category. Error: {e}")