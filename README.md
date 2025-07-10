# watchos-books

This repository contains JSON conversions of EPUB books for use on watchOS.

## Converting EPUB files

Use the provided `convert_epub.py` script to convert an EPUB file into the required JSON format.

### Usage

```bash
python3 convert_epub.py path/to/book.epub output.json
```

The script extracts the title, author, and chapters from the EPUB file and writes them to `output.json`.

### Dependencies

The script requires Python 3 and the following packages:

- `ebooklib`
- `beautifulsoup4`
- `lxml`

Install them with pip:

```bash
pip3 install --user ebooklib beautifulsoup4 lxml
```
