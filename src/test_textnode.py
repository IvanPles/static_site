import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

from md_inline import (split_nodes_delimiter, 
        extract_markdown_images, 
        extract_markdown_links, 
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)


class TestExtractMD(unittest.TestCase):

    def test_delim_bold_multiword(self):
        node = TextNode(
               "This is text with a **bolded word** and **another**", text_type_text
            )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/zjjcJKZ.png) and ![another](https://storage.googleapis.com/dfsdkjfd.png)"
        expected_res = [("image", "https://storage.googleapis.com/zjjcJKZ.png"),
                        ("another", "https://storage.googleapis.com/dfsdkjfd.png") ]
        res = extract_markdown_images(text)
        for el, el2 in zip(res, expected_res):
            self.assertEqual(el, el2)

    def test_extract_links(self):
            text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
            expected_res = [("link", "https://www.example.com"),
                            ("another", "https://www.example.com/another") ]
            res = extract_markdown_links(text)
            for el, el2 in zip(res, expected_res):
                self.assertEqual(el, el2)

    def test_split_links(self):
        node = TextNode("link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text)
        new_nodes = split_nodes_link([node])
        expected_res = [
                TextNode("link ", text_type_text),
                TextNode("to boot dev", text_type_link, url="https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("to youtube", text_type_link, url="https://www.youtube.com/@bootdotdev"),
        ]
        for el, el2 in zip(new_nodes, expected_res):
            self.assertEqual(el, el2)

    def test_split_images(self):
        node = TextNode("image ![to boot dev](img1.png) and ![another](img2.png)",
            text_type_text)
        new_nodes = split_nodes_image([node])
        expected_res = [
                TextNode("image ", text_type_text),
                TextNode("to boot dev", text_type_image, url="img1.png"),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_image, url="img2.png"),
        ]
        for el, el2 in zip(new_nodes, expected_res):
            self.assertEqual(el, el2)

    def test_total_split(self):
        text = f"This is **text** with an *italic* word and a `code block` "\
        f"and an ![image](img.png) and a [link](https://boot.dev)"
        expected_res = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "img.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            ]
        res = text_to_textnodes(text)
        # print(res)
        self.assertListEqual(res, expected_res)


if __name__ == "__main__":
    unittest.main()
