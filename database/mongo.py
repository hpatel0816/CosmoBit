import os

from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_COSMOBIT_URI')

def get_database():
    try:
        print("Connecting with database...")
        client = MongoClient(MONGO_URI)
        db = client['articles-db']
        print("Connected successfully.")
        return db
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None


def get_articles_collection(db):
    try:
        return db['articles']
    except Exception as e:
        print(f"Failed to access articles collection: {e}")
        return None


def get_categories_collection(db):
    try:
        return db['categories']
    except Exception as e:
        print(f"Failed to access categories collection: {e}")
        return None


def save_category_list(db, category_list):
    categories_collection = get_categories_collection(db)
    if categories_collection is not None:
        try:
            categories_collection.insert_many(category_list)
            print("Category list saved successfully.")
        except Exception as e:
            print(f"Failed to save category list: {e}")


def save_article(db, article):
    articles_collection = get_articles_collection(db)
    if articles_collection is not None:
        try:
            articles_collection.insert_one(article)
            print("Article saved successfully.")
        except Exception as e:
            print(f"Failed to save article: {e}")