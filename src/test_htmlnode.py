import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        res_str = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), res_str)

class TestLeafNode(unittest.TestCase):
    def test_leaf(self):
        node = LeafNode("This is a paragraph of text.", tag="p")
        node2 = LeafNode("Click me!", tag="a", props={"href": "https://www.google.com"})
        print(node2.to_html())
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
    def test_parent(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("Bold text", tag="b"),
                    LeafNode("Normal text"),
                    LeafNode("italic text", tag="i"),
                    LeafNode("Normal text"),
                ])
        res = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        print(node.to_html())
        self.assertEqual(node.to_html(), res)

if __name__ == "__main__":
    unittest.main()
