"""
Logging
"""
import dfraw.debug
import sys

enabled = True
output = sys.stdout

def log(*args):
	if enabled:
		output.write(''.join([str(i) for i in args]))
		output.write('\n')

