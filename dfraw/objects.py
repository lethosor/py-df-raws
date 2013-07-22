"""
objects

Basic classes for working with raws
"""

# Python 2 compatibiity
from __future__ import division
__metaclass__ = type

import dfraw.debug as debug

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

""" Exceptions """
class ParseError(Exception): pass

class File:
	"""
	A raw file
	"""
	def __init__(self, path):
		self.raw_string = ""
		f = open(path)
		self.raw_string = f.read()
		f.close()
		self.token_list = TokenList(self.raw_string)
		
		self.object_list = ObjectList(self.token_list)

class Token:
	def __init__(self, string):
		if len(string) and string[0] == '[' and string[-1] == ']':
			self.type = Token.TAG
		else:
			self.type = Token.COMMENT
		self.value = string
		if self.value.replace('\n','').replace('\t','').replace('\r','').replace(' ','') == '':
			self.value = ''
		if self.type == Token.TAG:
			self.list = self.value[1:-1].split(':')
		
	def __str__(self):
		return self.value
	
	def __repr__(self):
		return "<{0}>: {1}".format((None,'Tag','Comment')[self.type], self.value)
	
	def __getitem__(self, index):
		if self.type == Token.COMMENT:
			# Comment; acts like a string
			return self.value[index]
		else:
			try:
				return self.list[index]
			except IndexError:
				return None
		
	
# Constants
Token.TAG = 1
Token.COMMENT = 2
	
class TokenList:
	def __init__(self, string):
		"""
		Takes a string and returns a list of Token objects
		"""
		
		# Use the \x01 character to mark the ends of tags
		string = string.replace('\x01','').replace('[','\x01[').replace(']',']\x01')
		self.list = string.split('\x01')
		
		
		
		# Remove blank comments
		for i, token in enumerate(self.list):
			if token.type == Token.COMMENT and token.value == '':
				del self.list[i]
		
		
	def __getitem__(self, index):
		return self.list[index]
	
	def __len__(self):
		return len(self.list)	
		
class Object:
	def __init__(self, tokens):
		self.list = tokens
		self.flags = ObjectGetterFlags(tokens)
		self.tags = ObjectGetterTags(tokens)
		self.all_tags = ObjectGetterAllTags(tokens)
		self.name = self.tags.name
	
	def __getitem__(self, tag):
		"""
		Get a tag with type detection
		Returns:
		* False if the tag does not exist
		* True if the tag exists with no arguments
		* The tag's first argument, if the tag has only one argument
		* All of the tag's arguments, if the tag has multiple arguments
		* All of the tag's occurences' arguments, if more than 1 occurence
		"""
		result = self.all_tags[tag]
		if self.tags[tag] == False:
			# Tag does not occur at all
			return False
		elif result == [[]]:
			# Tag occurs once with no arguments
			return True
		elif len(result[0]) == 1:
			# Only 1 occurence, which has only 1 argument
			return result[0][0]
		elif len(result) == 1:
			# Only 1 occurence of tag
			return result[0]
		# Something else
		return result
	__getattr__ = __getitem__
	
class ObjectGetterFlags:
	def __init__(self, tokens):
		self.tokens = tokens
	def __getitem__(self, tag):
		# Returns True if the given tag name exists, False otherwise
		tag = tag.upper()
		for t in self.tokens:
			if t.type == Token.TAG and t[0] == tag:
				return True
		return False
	# Use the same functionality for attributes
	__getattr__ = __getitem__

class ObjectGetterTags:
	"""
	An object that allows access to tags with arguments via bracket/attribute
	syntax
	Returns a list of arguments if found, an empty list if no arguments, or 
	False if no matching tag
	"""
	def __init__(self, tokens):
		self.tokens = tokens
	def __getitem__(self, tag):
		"""
		Returns all arguments of the given tag
		"""
		tag = tag.upper()
		for t in self.tokens:
			if t.type == Token.TAG and t[0] == tag:
				return t[1:]
		return False
	# Use the same functionality for attributes
	__getattr__ = __getitem__
	
class ObjectGetterAllTags:
	"""
	Similar to ObjectGetterTags, but returns a list with all matching tags
	"""
	def __init__(self, tokens):
		self.tokens = tokens
	def __getitem__(self, tag):
		"""
		Returns a list of all matching tags
		"""
		list = []
		tag = tag.upper()
		for t in self.tokens:
			if t.type == Token.TAG and t[0] == tag:
				list.append(t[1:])
		return list
	# Use the same functionality for attributes
	__getattr__ = __getitem__


class ObjectList:
	def __init__(self, token_list):
		for i, token in enumerate(token_list):
			if token[0] == 'OBJECT':
				self.delimiter = token[1]
				start = i + 1
				break
		self.file_header = token_list[0].value.split('\n')[0]
		
		# A list of the starting locations of objects
		self.starts = []
		for i, token in enumerate(token_list):
			if i< start:
				continue
			if token[0] in (self.delimiter, self.file_header.upper()):
				debug.log('Found object: ',token)
				# Include all comments before the first tag 
				j = i-1
				while token_list[j].type != Token.TAG:
					j -= 1
				j += 1
				self.starts.append(j)
		
		t_list = []
		for i, v in enumerate(self.starts):
			t_list.append(token_list[v:self.starts[i+1] if i+1 < len(self.starts) else None])
		self.t_list = t_list
		
		self.list = []
		for tokens in self.t_list:
			self.list.append(Object(tokens))
		
	def __getitem__(self, index):
		"""
		Returns:
		* Object at the given index in self.list, if it exists
		* Object with the given name in self.list, if exists
		
		Raises IndexError otherwise
		"""	
		if index < len(self.list) and index >= 0:
			return self.list[int(index)]
		for obj in self.list:
			# Names are lowercase in DF
			if index.lower() in obj.name:
				return obj
		raise IndexError('Object not found in object list: {0}'.format(index))
	__getattr__ = __getitem__
		

