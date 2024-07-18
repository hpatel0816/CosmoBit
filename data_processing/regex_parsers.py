import re

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