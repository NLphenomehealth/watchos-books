import sys
import json
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "lxml")

    # Remove script and style elements
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    # Replace br with newline
    for br in soup.find_all('br'):
        br.replace_with('\n')

    # Append double newline after paragraphs and divs for readability
    for tag in soup.find_all(['p', 'div']):
        if tag.text.strip():
            tag.append('\n\n')

    text = soup.get_text()
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    text = '\n\n'.join(chunk.strip() for chunk in text.split('\n\n') if chunk.strip())
    return text


def convert_epub_to_json(epub_path):
    book = epub.read_epub(epub_path)

    title = book.get_metadata('DC', 'title')
    title = title[0][0] if title else epub_path

    author = book.get_metadata('DC', 'creator')
    author = author[0][0] if author else 'Unknown Author'

    chapters = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        if not isinstance(item, epub.EpubHtml):
            continue
        chapter_title = item.get_name()
        text = extract_text_from_html(item.get_content().decode('utf-8', errors='ignore'))
        if text.strip():
            chapters.append({
                'title': chapter_title,
                'content': text
            })

    return {
        'title': title,
        'author': author,
        'chapters': chapters
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_epub.py <file.epub> [output.json]")
        sys.exit(1)
    epub_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    data = convert_epub_to_json(epub_file)
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_data)
    else:
        print(json_data)


if __name__ == '__main__':
    main()
