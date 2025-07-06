from enum import Enum
from htmlnode import LeafNode
from typing import List
import re
class TextType(Enum):

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    


def text_node_to_html_node(text_node):
          

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
        
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
        
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
            
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
        
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
    

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, new_text_type: TextType) -> List[TextNode]:
    new_nodes = []

    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        i = 0
        while i < len(parts):
            text = parts[i]
            if text:
                
                node_type = new_text_type if i % 2 == 1 else TextType.TEXT
                new_nodes.append(TextNode(text, node_type))
            i += 1

    return new_nodes

def extract_markdown_images(text):
    
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches



def split_nodes_link(old_nodes: List['TextNode']) -> List['TextNode']:
    new_nodes = []
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        last_index = 0
        
        for match in re.finditer(pattern, text):
            start, end = match.span()
            anchor_text, url = match.groups()
            
            if start > last_index:
                before = text[last_index:start]
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            last_index = end
        
        if last_index < len(text):
            after = text[last_index:]
            new_nodes.append(TextNode(after, TextType.TEXT))
    
    return new_nodes


def split_nodes_image(old_nodes: List['TextNode']) -> List['TextNode']:
    new_nodes = []
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        last_index = 0
        
        for match in re.finditer(pattern, text):
            start, end = match.span()
            alt_text, url = match.groups()
            
            
            if start > last_index:
                before = text[last_index:start]
                new_nodes.append(TextNode(before, TextType.TEXT))
        
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            last_index = end
  
        if last_index < len(text):
            after = text[last_index:]
            new_nodes.append(TextNode(after, TextType.TEXT))
    
    return new_nodes

def split_images(text):
    
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    result = []
    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            result.append((text[last_end:start], TextType.TEXT))
        alt, url = match.groups()
        result.append((alt, TextType.IMAGE, url))
        last_end = end
    if last_end < len(text):
        result.append((text[last_end:], TextType.TEXT))
    return result

def split_links(text):
    
    pattern = re.compile(r'\[(.*?)\]\((.*?)\)')
    result = []
    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            result.append((text[last_end:start], TextType.TEXT))
        link_text, url = match.groups()
        result.append((link_text, TextType.LINK, url))
        last_end = end
    if last_end < len(text):
        result.append((text[last_end:], TextType.TEXT))
    return result

def split_bold(text):
   
    pattern = re.compile(r'\*\*(.*?)\*\*')
    result = []
    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            result.append((text[last_end:start], TextType.TEXT))
        result.append((match.group(1), TextType.BOLD))
        last_end = end
    if last_end < len(text):
        result.append((text[last_end:], TextType.TEXT))
    return result

def split_italic(text):
  
    pattern = re.compile(r'_(.*?)_')
    result = []
    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            result.append((text[last_end:start], TextType.TEXT))
        result.append((match.group(1), TextType.ITALIC))
        last_end = end
    if last_end < len(text):
        result.append((text[last_end:], TextType.TEXT))
    return result

def split_code(text):
    
    pattern = re.compile(r'`(.*?)`')
    result = []
    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            result.append((text[last_end:start], TextType.TEXT))
        result.append((match.group(1), TextType.CODE))
        last_end = end
    if last_end < len(text):
        result.append((text[last_end:], TextType.TEXT))
    return result




def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    splitters = [split_nodes_image, split_nodes_link,
                 lambda nodes: split_nodes_delimiter(nodes, "**", TextType.BOLD),
                 lambda nodes: split_nodes_delimiter(nodes, "_", TextType.ITALIC),
                 lambda nodes: split_nodes_delimiter(nodes, "`", TextType.CODE)]

    for splitter in splitters:
        nodes = splitter(nodes)

    return nodes

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith('# ') or block.startswith('## ') or block.startswith('### ') or block.startswith('#### ') or block.startswith('##### ') or block.startswith('###### '):
        return BlockType.HEADING
    
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    lines = block.split('\n')
    
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    
    result = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            result.append(stripped_block)
    
    return result






