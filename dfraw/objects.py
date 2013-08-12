"""
Objects
"""

__metaclass__ = type

class Token:
    def __new__(cls, text, *args, **kwargs):
        if cls != Token:
            return object.__new__(cls)
        if text.startswith('[') and text.endswith(']'):
            return TagToken(text, *args, **kwargs)
        else:
            return CommentToken(text, *args, **kwargs)
    
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, repr(str(self)))
    
    
class TagToken(Token):    
    def __init__(self, text):
        self.value = text[1:-1].split(':')
    
    def __unicode__(self):
        return '[' + ':'.join(self.value) + ']'
    __str__ = __unicode__
    
    
class CommentToken(Token):
    def __init__(self, text):
        self.value = text
    
    def __unicode__(self):
        return self.value
    __str__ = __unicode__


