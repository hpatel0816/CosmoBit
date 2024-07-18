import json
import logging
import os

from .regex_parsers import clean_text, handle_newlines_and_references, format_figures, structure_text


def process_all_articles(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                article_data = json.load(f)
            processed_data = process_article_data(article_data)
            output_file_path = os.path.join(output_dir, file_name)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)
            logging.info(f"Processed data saved to {output_file_path}")


def process_article_data(article_data):
    # Remove all extra spacing, handle special characters and figures, and ensure clear consistent formatting of data
    processed_data = {}
    content = article_data["content"]
    for key, value in content.items():
        cleaned_text = format_figures(value)
        cleaned_text = handle_newlines_and_references(cleaned_text)
        structured_text = structure_text(cleaned_text)
        cleaned_text = clean_text(structured_text)
        processed_data[key] = cleaned_text
    return processed_data

