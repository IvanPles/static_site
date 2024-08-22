from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from md_inline import text_to_textnodes, text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [el.strip() for el in blocks if len(el.replace("\n", ""))]
    return blocks

def block_to_block_type(block):
    if any(block.startswith("#"*ix+" ") for ix in range(1,7)):
        return block_type_heading
    if block[0:3] == "```" and block[-3:] == "```":
        return block_type_code
    lines = block.split("\n")
    if all(l[0:2] == "> " for l in lines):
        return block_type_quote
    if all(l[0:2] == "* " for l in lines) or all(l[0:2] == "- " for l in lines):
        return block_type_unordered_list
    if all(l[:len(f"{ix}. ")] == f"{ix+1}. " for ix, l in enumerate(lines) ):
        return block_type_ordered_list
    return block_type_paragraph

def text_to_html_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_nodes

def create_paragraph_html_node(block):
    html_nodes = text_to_html_children(block)
    parent_html = ParentNode(tag="p", children=html_nodes)
    return parent_html

def create_heading_html_node(block):
    i_h = 0
    for ch in block:
        if ch == "#":
            i_h+=1
        else:
            break
    html_nodes = text_to_html_children(block[i_h+1:])
    parent_html = ParentNode(tag=f"h{i_h}", children=html_nodes)
    return parent_html

def create_quote_html_node(block):
    print(block)
    block_proc = "\n".join([line[2:] for line in block.split("\n")])
    html_nodes = []
    for bl in block_proc:
        html_nodes.extend(text_to_html_children(bl))
    parent_html = ParentNode(tag=f"blockquote", children=html_nodes)
    return parent_html

def create_code_html_node(block):
    html_nodes = text_to_html_children(block[3:-3].strip())
    code_html = ParentNode(tag=f"code", children=html_nodes)
    parent_html = ParentNode(tag = "pre", children = [code_html])
    return parent_html

def create_ordered_list_html_node(block):
    html_nodes_lines = [text_to_html_children(line.lstrip(f"{ix+1}. ")) 
        for ix, line in enumerate(block.split("\n"))]
    html_nodes_lines = [ParentNode(tag="li", children=html_nodes_line)
                        for html_nodes_line in html_nodes_lines]
    parent_html = ParentNode(tag=f"ol", 
                             children=html_nodes_lines)
    return parent_html

def create_unordered_list_html_node(block):
    html_nodes_lines = [text_to_html_children(line[2:]) for line in block.split("\n")]
    html_nodes_lines = [ParentNode(tag="li", children=html_nodes_line)
                        for html_nodes_line in html_nodes_lines]
    parent_html = ParentNode(tag=f"ul", 
                             children=html_nodes_lines)
    return parent_html

block_type_func_maping = {
    block_type_paragraph: create_paragraph_html_node,
    block_type_heading: create_heading_html_node,
    block_type_code: create_code_html_node,
    block_type_quote: create_quote_html_node,
    block_type_ordered_list: create_ordered_list_html_node,
    block_type_unordered_list: create_unordered_list_html_node,
}

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = [] 
    print(blocks)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes.append(block_type_func_maping[block_type](block))
    ###
    root_node = ParentNode(tag="div", children=html_nodes)
    print(root_node.to_html())
    return root_node

