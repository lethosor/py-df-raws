"""
Tests for dfraw.objects
"""

import unittest

import dfraw

class ObjectsTest(unittest.TestCase):
    def setUp(self):
        self.comment_tokens = ('a', ' \n', '', 'This is a comment', '[', ']', ':')
        self.tag_tokens = ('[a]', '[]', '[This:is:a:tag]', '[a:b]', '[:]')
    
    def test_tag_tokens(self):
        for t in self.tag_tokens:
            token = dfraw.objects.Token(t)
            self.assertIsInstance(token, dfraw.objects.TagToken)
            self.assertEqual(t, str(token))
    
    def test_comment_tokens(self):
        for t in self.comment_tokens:
            token = dfraw.objects.Token(t)
            self.assertIsInstance(token, dfraw.objects.CommentToken)
            self.assertEqual(t, str(token))
    
if __name__ == '__main__':
    unittest.main()
