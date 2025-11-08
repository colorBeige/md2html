# md2html

Converting markdown to HTML.

## Usage

Move to the file directory containing the python file.

Usage: 
```bash
python md2html.py <input.md> [output.html]
```

input.md is required and output.html is optional.

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
