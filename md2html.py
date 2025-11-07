import sys
from pathlib import Path

def convert_emphasis(text: str) -> str:
    pass

def convert_paragraph(text: str) -> str:
    pass

def convert_headings(text: str) -> str:
    pass

def convert_ordered_list(text: str) -> str:
    pass

def convert_unordered_list(text: str) -> str:
    pass

def convert_code(text: str) -> str:
    pass

def convert_link(text: str) -> str:
    pass

def convert(text: str) -> str:
    pass

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
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