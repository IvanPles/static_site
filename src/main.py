from file_processing import process_files
from content_generation import generate_page

if __name__ == "__main__":
    process_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

