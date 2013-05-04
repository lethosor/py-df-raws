"""
objects

Basic classes for working with raws
"""

# Python 2 compatibiity
from __future__ import division
__metaclass__ = type

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
	

class Token:
	def __init__(self, string):
		if len(string) and string[0] == '[' and string[-1] == ']':
			self.type = Token.TAG
		else:
			self.type = Token.COMMENT
		self.value = string
		if self.value.replace('\n','').replace('\t','').replace('\r','') == '':
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
			return self.list[index]
		
	
# Constants
Token.TAG = 1
Token.COMMENT = 2
	
class TokenList:
	def __init__	(self, string):
		"""
		Takes a string and returns a list of Token objects
		"""
		#string = string.replace('[','[[').replace(']',']]')
		self.list = []
		i = j = 0
		tag = False
		while i-1 < len(string):
			#print i, j, tag, arr
			if tag:
				# Inside a tag
				try:
					j = string.index(']', i)
				except ValueError:
					# No ] found, so bad syntax
					raise ParseError('No closing bracket ( ] ) found! (char %i)' % i)
				# Include the brackets
				self.list.append(Token(string[i-1:j+1]))
				# Jump to the last ]
				i = j
				tag = False
				
			else:
				# Inside a comment
				try:
					j = string.index('[', i)
				except ValueError:
					# No [ found, which is perfectly valid at the end of a file
					j = len(string)
				# Exclude the next [
				self.list.append(Token(string[(i+1 if i>0 else i):j]))
				# Jump to 1 character after the next [
				i = j + 1
				tag = True
				
		# Remove blank comments
		for i, token in enumerate(self.list):
			if token.type == Token.COMMENT and token.value == '':
				del self.list[i]
	
	def __getitem__(self, index):
		return self.list[index]	
		
		

