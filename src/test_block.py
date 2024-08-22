import unittest
from md_block import (
        markdown_to_blocks,
        markdown_to_html_node,
        block_to_block_type,
        block_type_paragraph,
        block_type_heading,
        block_type_ordered_list,
        block_type_unordered_list,
        block_type_code,
        block_type_quote
)


class TestExtractBlock(unittest.TestCase):

    def test_extract_blocks(self):

        text = f"# This is a heading\n\n"\
            f"This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"\
            f"* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(text)
 
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ],
            blocks,
        )

    def test_delim_bold_multiword(self):

        text = f"# This is a heading\n\n"\
            f"This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"\
            f"* This is the first list item in a list block\n* This is a list item\n"\
            f"* This is another list item\n\n"\
            f"1. ordered list\n2. ordered list again\n\n"\
            f"```Some code here```"
        blocks = markdown_to_blocks(text)
        block_types = [block_to_block_type(b) for b in blocks]
 
        self.assertListEqual(
            [
                block_type_heading,
                block_type_paragraph,
                block_type_unordered_list,
                block_type_ordered_list,
                block_type_code
            ],
            block_types,
        )
    def test_markdown_to_html_node(self):
        text = f"# This is a heading\n\n"\
            f"This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"\
            f"* This is the first list item in a list block\n* This is a list item\n"\
            f"* This is another list item\n\n"\
            f"1. ordered list\n2. ordered list again\n\n"\
            f"```Some code here```"
        html_node = markdown_to_html_node(text)
        print(html_node.to_html())
        expected_res = f"<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p>"\
                f"<ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul>"\
                f"<ol><li>ordered list</li><li>ordered list again</li></ol><pre><code>Some code here</code></pre></div>"

        self.assertEqual(html_node.to_html(), expected_res)



if __name__ == "__main__":
    unittest.main()
