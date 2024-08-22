import os

from md_block import markdown_to_html_node
from file_processing import get_all_files_recursive, change_top_folder

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No header in markdown")

def generate_page(src_path, template_path, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    with open(src_path, "r") as f:
        md_data = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(md_data)
    html_nodes = markdown_to_html_node(md_data)
    html_cotent = html_nodes.to_html()
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_cotent)
    with open(dst_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(content_path, template_path, dst_path):
    folders, content_files = get_all_files_recursive(content_path)
    new_folders, html_files = change_top_folder(folders, content_files, dst_path)
    html_files = [f.replace(".md", ".html") for f in html_files if f.endswith(".md")]
    for folder in new_folders:
        os.mkdir(folder)
    for content_file, html_file in zip(content_files, html_files):
        generate_page(content_file, template_path, html_file)

