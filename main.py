import json
import time
import logging

from web_scraper.category_scraper import CategoryScraper
from web_scraper.article_scraper import ArticleScraper
from data_processing.process import process_all_articles
from database.mongo import get_database, save_category_list, save_article

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

    db = get_database()
    if db is None:
        logging.error("Failed to connect to the database. Exiting.")
        exit(1)

    for category in CATEGORIES:
        try:
            logging.info(f"Scraping category: {category}")
            articles = category_scraper.scrape_category(f"{NATURE_BASE_URL}{category}")

            if articles:
                # json_file_path = f"nature_{category.replace('-', '_')}.json"
                # save_to_json(articles, json_file_path)
                save_category_list(db, articles)
                logging.info(f"The {category} category data was saved to the databse")

                for article in articles:
                    # TODO: Setup scraping and processing for other types of data (News, Highlights, etc)
                    if article['Type'] == 'Research':
                        try:
                            article_url = article['Link']
                            is_open_access = article['OpenAccess']
                            logging.info(f"Scraping article: {article_url}")
                            article_data = article_scraper.scrape_article(article_url, is_open_access)
                            if article_data:
                                # article_id = article_url.split('/')[-1]
                                # article_json_path = f"articles/article_{article_id}_data.json"
                                # save_to_json(article_data, article_json_path)
                                save_article(db, article_data)
                                logging.info(f"Article data saved to database.")
                                # Wait 1.5 seconds before scraping the next article
                            time.sleep(1)
                        except Exception as e:
                            logging.error(f"Failed to scrape the {article} article. Error: {e}")
            # Wait 5 seconds before scraping the next category
            time.sleep(5)
        except Exception as e:
            logging.error(f"Failed to scrape the {category} category. Error: {e}")
    
    # Process all scraped articles
    # logging.info("Processing all scraped articles")
    # process_all_articles('articles', 'processed_articles')
    # logging.info("All articles processed")