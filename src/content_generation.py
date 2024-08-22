from md_block import mardown_to_html_node

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
    html_nodes = mardown_to_html_node(md_data)
    html_cotent = html_nodes.to_html()
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_cotent)
    with open(dst_path, "w") as f:
        f.write(final_html)

