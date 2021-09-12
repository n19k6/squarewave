import unittest
from string_helper import add_two_strings

class FunctionTestCase(unittest.TestCase):
    """Tests for 'string_helper'"""
    
    def test_add_two_different_strings(self):
        """Can two strings be concatinated?"""
        concatinated_string = add_two_strings("Albert", "Einstein")
        self.assertEqual("Albert Einstein", concatinated_string)
        
unittest.main()
