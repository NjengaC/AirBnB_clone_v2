from bs4 import BeautifulSoup

def uppercase_tags(html_file, output_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Convert all tags to uppercase
    for tag in soup.find_all():
        tag.name = tag.name.upper()

    # Write modified HTML to output file
    with open(output_file, 'w') as f:
        f.write(str(soup))

if __name__ == "__main__":
    input_html_file = input("Enter the path to the HTML file: ")
    output_html_file = input("Enter the path for the output HTML file: ")

    uppercase_tags(input_html_file, output_html_file)
    print("Tags converted to uppercase and saved to", output_html_file)
