# md2html

Converting markdown to HTML.

## Usage

Move to the file directory containing the python file.

Usage: `python md2html.py <input.md> [output.html]`

## Supported Markdown Features

- **Headings**: `# Header` and `Header\n====` styles (h1-h6)
- **Emphasis**: `*italic*`, `**bold**`, `***bold italic***` (+ underscore variants)
- **Lists**: Ordered `1. item` and unordered `- item` / `* item` / `+ item`
- **Code**: Inline `` `code` `` with backticks
- **Links**: `[text](url)` format
- **Paragraphs**: Text blocks with `<br>` line breaks

## Environment Setup

In your terminal: 

```bash
conda env create -f environment.yml
conda activate markdown
```

## Testing with pytest

In your terminal: 

```bash
pytest test_md2html.py -v     # Run all 62 tests with verbose output
pytest test_md2html.py        # Run tests quietly
```

## Limitations
- Empty heading and list items are not converted.
- No nested lists
- Blank lines between paragraphs aren't preserved
