import re
import sys
from pathlib import Path

def convert_emphasis(text: str) -> str:
    #3. Emphasis bold, italics, or both

    # Asterisks can be within words
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<em><strong>\1</strong></em>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

    # Underscore cannot be within words/characters
    text = re.sub(r'(?<!\w)___(.*?)___(?!\w)', r'<em><strong>\1</strong></em>', text)
    text = re.sub(r'(?<!\w)__(.*?)__(?!\w)', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\w)_(.*?)_(?!\w)', r'<em>\1</em>', text)

    return text

def convert_paragraph(text: str) -> str:
    # 2. Paragraphs - blank line that separates text blocks
    lines = text.split('\n')
    result = []
    current_paragraph = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Ignore lines that are already HTML tags or empty lines
        is_html_line = (
            stripped_line.startswith('<h') and stripped_line.endswith('>') or
            stripped_line.startswith('<ol>') or stripped_line.startswith('</ol>') or
            stripped_line.startswith('<ul>') or stripped_line.startswith('</ul>') or
            stripped_line.startswith('<li>') or stripped_line.startswith('</li>') or
            stripped_line == ''
        )
        
        if is_html_line:
            # If we hit an HTML line, add line breaks for more than one line
            # then wrap it in <p> tags and reset
            if current_paragraph:
                paragraph_content = '<br>'.join(current_paragraph)
                result.append(f'<p>{paragraph_content}</p>')
                current_paragraph = []
            
            # Remove unnecsessary empty lines and keep original lines
            if stripped_line:
                result.append(line)
        else:
            # Text - may have multiple lines - add for future breaks
            current_paragraph.append(stripped_line)
    
    # Finish any remaining paragraph left in the end
    if current_paragraph:
        paragraph_content = '<br>'.join(current_paragraph)
        result.append(f'<p>{paragraph_content}</p>')
    
    return '\n'.join(result)

def convert_headings(text: str) -> str:
    # 1. Headings with #, =, and -
    lines = text.split('\n')
    #print(lines)
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for # headings with a single space
        match = re.match(r'^(#{1,6}) (.+)', line)
        if match:
            level = len(match.group(1))
            text = match.group(2)
            result.append(f'<h{level}>{text}</h{level}>')
            i += 1
            continue
        
        # Check the line after for = (h1) and - (h2)
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            # at least two = for level 1 heading
            if re.match(r'^={2,}$', next_line):
                result.append(f'<h1>{line}</h1>')
                i += 2
                continue
            # at least two - for level 2 heading
            elif re.match(r'^-{2,}$', next_line):
                result.append(f'<h2>{line}</h2>')
                i += 2
                continue
        
        # Normal text
        result.append(line)
        i += 1
    
    return '\n'.join(result)

def convert_ordered_list(text: str) -> str:
    # 4. Ordered lists (lines starting with number. and single space)
    lines = text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        match = re.match(r'^\d+\. (.+)', line)
        if match:
            # Start a new list if not already in one and append list item
            if not in_list:
                result.append('<ol>')
                in_list = True
            text = match.group(1)
            result.append(f'  <li>{text}</li>')
        else:
            # Close list if we were in one, then append the non-list line
            if in_list:
                result.append('</ol>')
                in_list = False
            result.append(line)
    
    # Close the list if it was still open at the end
    if in_list:
        result.append('</ol>')
    
    return '\n'.join(result)

def convert_unordered_list(text: str) -> str:
    # 4. Unordered lists (lines starting with -, *, or + followed by single space)
    lines = text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        match = re.match(r'^[-*+] (.+)', line)
        if match:
            # Start a new list if not already in one and append list item
            if not in_list:
                result.append('<ul>')
                in_list = True
            text = match.group(1)
            result.append(f'  <li>{text}</li>')
        else:
            # Close list if we were in one, then append the non-list line
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    # Close the list if it was still open at the end
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

def convert_code(text: str) -> str:
    # 5. Code with single or double backticks
    text = re.sub(r'`{1,2}(.*?)`{1,2}', r'<code>\1</code>', text)
    return text

def convert_link(text: str) -> str:
    #6. Convert markdown links [text](url) to <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

def convert(text: str) -> str:
    text = convert_headings(text)
    text = convert_ordered_list(text)
    text = convert_unordered_list(text)
    text = convert_emphasis(text)
    text = convert_code(text)
    text = convert_link(text)
    text = convert_paragraph(text)

    return text

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python md2html.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        input_path = Path(input_file)
        output_file = input_path.with_suffix('.html')
    
    try:
        with open(input_file, 'r') as f:
            markdown_input = f.read()

        html_output = convert(markdown_input)

        with open(output_file, 'w') as f:
            f.write(html_output)

    except FileNotFoundError:
        print(f"Input file {input_file} not found.")
        sys.exit(1)

    print("Done")

if __name__ == "__main__":
    main()