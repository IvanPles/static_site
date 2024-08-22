from file_processing import process_files
from content_generation import generate_pages_recursive

if __name__ == "__main__":
    process_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")

