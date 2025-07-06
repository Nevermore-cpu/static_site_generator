import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_with_single_attribute(self):
        """Test props_to_html with a single HTML attribute"""
        node = HTMLNode("p", "Hello world", None, {"class": "greeting"})
        result = node.props_to_html()
        self.assertEqual(result, ' class="greeting"')
    
    def test_props_to_html_with_multiple_attributes(self):
        """Test props_to_html with multiple HTML attributes"""
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "class": "link"
        }
        node = HTMLNode("a", "Click me!", None, props)
        result = node.props_to_html()
        
        # Check that all attributes are present
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('class="link"', result)
        
        # Check that it starts with a space
        self.assertTrue(result.startswith(' '))
    
    def test_props_to_html_with_no_attributes(self):
        """Test props_to_html with no attributes (None or empty dict)"""
        # Test with None props
        node1 = HTMLNode("div", "Content", None, None)
        result1 = node1.props_to_html()
        self.assertEqual(result1, "")
        
        # Test with empty dict props
        node2 = HTMLNode("div", "Content", None, {})
        result2 = node2.props_to_html()
        self.assertEqual(result2, "")
    
   
    
    def test_props_to_html_ordering_consistency(self):
        """Test that props_to_html produces consistent ordering"""
        props = {"z": "last", "a": "first", "m": "middle"}
        node = HTMLNode("div", "Content", None, props)
        result1 = node.props_to_html()
        result2 = node.props_to_html()
        
        # Should produce the same result each time
        self.assertEqual(result1, result2)
    
    def test_htmlnode_initialization(self):
        """Test HTMLNode can be initialized with different parameter combinations"""
        # Test with all parameters
        node1 = HTMLNode("div", "Hello", None, {"class": "container"})
        self.assertEqual(node1.tag, "div")
        self.assertEqual(node1.value, "Hello")
        self.assertEqual(node1.props, {"class": "container"})
        
        # Test with minimal parameters
        node2 = HTMLNode("p", "Text")
        self.assertEqual(node2.tag, "p")
        self.assertEqual(node2.value, "Text")
    
    def test_props_to_html_with_boolean_like_attributes(self):
        """Test props_to_html with boolean-like HTML attributes"""
        props = {
            "disabled": "disabled",
            "checked": "checked",
            "hidden": ""
        }
        node = HTMLNode("input", None, None, props)
        result = node.props_to_html()
        
        self.assertIn('disabled="disabled"', result)
        self.assertIn('checked="checked"', result)
        self.assertIn('hidden=""', result)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()