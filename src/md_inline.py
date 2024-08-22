import re
from htmlnode import LeafNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

create_node_mapping = {
    text_type_text: lambda t: LeafNode(t.text),
    text_type_bold: lambda t: LeafNode(t.text, tag="b"),
    text_type_italic: lambda t: LeafNode(t.text, tag="i"),
    text_type_code: lambda t: LeafNode(t.text, tag="code"),
    text_type_link: lambda t: LeafNode(t.text, tag="a", props={"href": t.url}),
    text_type_image: lambda t: LeafNode("", tag="img", props={"src": t.url, "alt": t.text})
}

def text_node_to_html_node(text_node):
    func = create_node_mapping.get(text_node.text_type, None)
    if func is None:
        raise ValueError(f"Invalid text type: {text_node.text_type}")
    return func(text_node)

def iterate_over_nodes_and_construct(old_nodes, func):
    new_nodes = []
    for old_node in old_nodes:
        add_nodes = func(old_node)
        new_nodes.extend(add_nodes)
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def splitting_by_delimiter(node):
        if node.text_type != text_type_text:
            return [node]
        splitted_text = node.text.split(delimiter)
        if len(splitted_text) % 2 == 0:
                raise ValueError("Invalid markdown")
        splitted_nodes = [TextNode(text, text_type) if i % 2 else TextNode(text, text_type_text) 
            for i, text in enumerate(splitted_text) if len(text)]
        return splitted_nodes
    #
    new_nodes = iterate_over_nodes_and_construct(old_nodes, splitting_by_delimiter)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text) 

def split_nodes_after_re(old_nodes, search_func, res_func, text_type):
    def splitting_by_search(node):
        if node.text_type != text_type_text:
            return [node]
        curr_text = node.text
        extracted = search_func(curr_text)
        add_nodes = []
        for el in extracted:
            splitted_text = curr_text.split(res_func(el[0], el[1]), 1)
            f_text = splitted_text[0]
            if len(f_text):
                add_nodes.append(TextNode(splitted_text[0], text_type_text))
            add_nodes.append(TextNode(el[0], text_type, url=el[1]))
            curr_text = splitted_text[1]
        if len(curr_text):
            add_nodes.append(TextNode(curr_text, text_type_text))
        return add_nodes
    #
    new_nodes = iterate_over_nodes_and_construct(old_nodes, splitting_by_search)
    return new_nodes

def split_nodes_image(old_nodes):
    func1 = lambda x, y: f"![{x}]({y})"
    new_nodes = split_nodes_after_re(old_nodes, extract_markdown_images, func1, text_type_image)
    return new_nodes

def split_nodes_link(old_nodes):
    func1 = lambda x, y: f"[{x}]({y})"
    new_nodes = split_nodes_after_re(old_nodes, extract_markdown_links, func1, text_type_link)
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, text_type_text)
    res_nodes = split_nodes_delimiter([text_node], "`", text_type_code)
    res_nodes = split_nodes_delimiter(res_nodes, "**", text_type_bold)
    res_nodes = split_nodes_delimiter(res_nodes, "*", text_type_italic)
    res_nodes = split_nodes_image(res_nodes)
    res_nodes = split_nodes_link(res_nodes)
    return res_nodes


