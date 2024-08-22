import sys
import requests
import io
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

def extract_pdf_content(url):
    response = requests.get(url)
    pdf_file = io.BytesIO(response.content)
    return extract_text(pdf_file, laparams=LAParams())

def parse_content(content):
    lines = content.split('\n')
    categories = {}
    current_category = None
    current_book = None

    for line in lines:
        line = line.strip()
        if line.isupper() and len(line) > 3:
            current_category = line
            categories[current_category] = []
        elif line and current_category:
            if ',' in line and ':' not in line:
                current_book = {'title': line.split(',')[0].strip(), 'author': line.split(',')[1].strip(), 'notes': ''}
                categories[current_category].append(current_book)
            elif current_book:
                current_book['notes'] += line + ' '

    return categories

def print_results(categories):
    for category, books in categories.items():
        print(f"\n## {category}")
        for book in books:
            print(f"\n**{book['title']}**")
            print(f"Author: {book['author']}")
            if book['notes']:
                print(f"Notes: {book['notes'].strip()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <pdf_url>")
        sys.exit(1)

    url = sys.argv[1]
    content = extract_pdf_content(url)
    categories = parse_content(content)
    print_results(categories)
