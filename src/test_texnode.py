import unittest

from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes, block_to_block_type, BlockType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a nothing", TextType.ITALIC)
        self.assertNotEqual(node, node2)



    def test_text(self):
    
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



def test_split_basic_code():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]

def test_split_bold_double_asterisk():
    node = TextNode("This has **bold** text here", TextType.TEXT)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert result == [
        TextNode("This has ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text here", TextType.TEXT),
    ]

def test_split_italic_underscore():
    node = TextNode("Some _italic_ words", TextType.TEXT)
    result = split_nodes_delimiter([node], "_", TextType.ITALIC)
    assert result == [
        TextNode("Some ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" words", TextType.TEXT),
    ]

def test_no_delimiter_present():
    node = TextNode("Just plain text", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [TextNode("Just plain text", TextType.TEXT)]

def test_multiple_inline_matches():
    node = TextNode("First `one` and second `two`.", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [
        TextNode("First ", TextType.TEXT),
        TextNode("one", TextType.CODE),
        TextNode(" and second ", TextType.TEXT),
        TextNode("two", TextType.CODE),
        TextNode(".", TextType.TEXT),
    ]

def test_starting_with_delimiter():
    node = TextNode("`start` then text", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [
        TextNode("start", TextType.CODE),
        TextNode(" then text", TextType.TEXT),
    ]

def test_ending_with_delimiter():
    node = TextNode("text ends with `final`", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [
        TextNode("text ends with ", TextType.TEXT),
        TextNode("final", TextType.CODE),
    ]

def test_unmatched_delimiter_no_closing():
    node = TextNode("This has `an unmatched delimiter", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [
        TextNode("This has ", TextType.TEXT),
        TextNode("an unmatched delimiter", TextType.CODE),
    ]

def test_empty_string():
    node = TextNode("", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == []

def test_multiple_nodes_some_non_text():
    nodes = [
        TextNode("First `one`.", TextType.TEXT),
        TextNode("This is bold", TextType.BOLD),  # Should remain unchanged
        TextNode("Second `two`.", TextType.TEXT),
    ]
    result = split_nodes_delimiter(nodes, "`", TextType.CODE)
    assert result == [
        TextNode("First ", TextType.TEXT),
        TextNode("one", TextType.CODE),
        TextNode(".", TextType.TEXT),
        TextNode("This is bold", TextType.BOLD),
        TextNode("Second ", TextType.TEXT),
        TextNode("two", TextType.CODE),
        TextNode(".", TextType.TEXT),
    ]

def test_consecutive_delimiters_empty_segment():
    node = TextNode("Text with `` empty `` code block", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert result == [
        TextNode("Text with ", TextType.TEXT),
        TextNode("", TextType.CODE),
        TextNode(" empty ", TextType.TEXT),
        TextNode("", TextType.CODE),
        TextNode(" code block", TextType.TEXT),
    ]


def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



def test_split_images(self):
    node = TextNode

class TestTextToTextNodes(unittest.TestCase):
    def test_example_input(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        result_nodes = text_to_textnodes(text)
        self.assertEqual(len(result_nodes), len(expected_nodes))

        for res, exp in zip(result_nodes, expected_nodes):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)
            self.assertEqual(res.url, exp.url)

    def test_plain_text_only(self):
        text = "Just some boring text."
        expected = [TextNode("Just some boring text.", TextType.TEXT)]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)
        self.assertIsNone(result[0].url)

    def test_multiple_bold_and_italic(self):
        text = "**bold1** and _italic1_ then **bold2** and _italic2_"
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic1", TextType.ITALIC),
            TextNode(" then ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic2", TextType.ITALIC),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )




class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_single_hash(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
    def test_heading_with_formatting(self):
        self.assertEqual(block_to_block_type("# **Bold** heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading with *italic*"), BlockType.HEADING)
    




def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )



if __name__ == "__main__":
    unittest.main()
