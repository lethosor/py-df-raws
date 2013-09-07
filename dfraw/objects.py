"""
Objects
"""

__metaclass__ = type

class Token:
    """
    A token (either a tag or comment).
    
    This class instantiates different token classes based on the value given.
    """
    def __new__(cls, text, *args, **kwargs):
        if cls != Token:
            return object.__new__(cls)
        if text.startswith('[') and text.endswith(']'):
            return TagToken(text, *args, **kwargs)
        else:
            return CommentToken(text, *args, **kwargs)
    
    def __repr__(self):
        """
        Returns a representation of this token (with legal Python syntax).
        
        >>> repr(TagToken('[foo]'))
        TagToken('foo')
        """
        return "{0}({1})".format(self.__class__.__name__, repr(str(self)))
    
    
class TagToken(Token):
    """
    A token that represents a tag.
    
    Examples: "[a:b]", "[foo]", "[spam:eggs:spam:spam]"
    """
    def __init__(self, text):
        # Initializes self.name and self.args
        self.value = text[1:-1].split(':')
    
    def __unicode__(self):
        """ The tag's original text """
        return '[' + ':'.join(self.value) + ']'
    __str__ = __unicode__
    
    @property
    def value(self):
        """ A list containing the tag's name and arguments """
        return [self.name] + self.args
    
    @value.setter
    def value(self, v):
        self.name, self.args = v[0], v[1:]

    
class CommentToken(Token):
    """
    A token that represents anything other than a tag (i.e. a comment).
    
    Example: "Example"
    """
    def __init__(self, text):
        self.value = text
    
    def __unicode__(self):
        """ The text of the comment """
        return self.value
    __str__ = __unicode__


