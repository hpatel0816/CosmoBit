import re
import json

def clean_text(text):
    # Replace newline characters with appropriate punctuation
    text = re.sub(r'(?<=\w)\n(?=\w)', '. ', text)  # Insert '. ' if no space on either side
    text = re.sub(r'\n+', ' ', text)  # Replace other newlines with space
    # Remove spaces before punctuation
    text = re.sub(r'\s+([.,;:?!])', r'\1', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def handle_newlines_and_references(text):
    # Remove numbers that have \n before and after them directly
    text = re.sub(r'\n\d+\n', '', text)
    # Replace newlines separating numbers or references with spaces
    text = re.sub(r'\s*\n\s*(\d+)\s*\n\s*', r' \1, ', text)
    return text

def format_figures(text):
    # Replace figure references with "Figure #" and ensure correct formatting
    text = re.sub(r'\(Fig\.?\s*\n?\d+\n?\)', lambda match: f"(Fig. {re.search(r'\d+', match.group()).group()})", text)
    return text

def structure_text(text):
    # Replace specific patterns with new lines or bullet points for lists
    text = re.sub(r'(?<=\w)\s{2,}(?=\w)', '\n\n', text)  # Paragraph breaks
    text = re.sub(r'\n+', '\n', text)  # Single newline
    return text


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


with open("../data/articles/raw_data/article_data.json", "r") as file:
    jsonData = json.load(file)

processed_data = process_article_data(jsonData)

with open('../data/articles/processed/article.json', 'w') as file:
    json.dump(processed_data, file)