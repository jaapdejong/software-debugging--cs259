#!/usr/bin/python
# Complete the program such that it prints
# out the actual contents of the code lines
# instead of the file name and line number
# 

import sys
import linecache

def remove_html_markup(s):
	tag   = False
	quote = False
	out   = ""

	for c in s:
		if c == '<' and not quote:
			tag = True
		elif c == '>' and not quote:
			tag = False
		elif c == '"':
			quote = not quote
		elif not tag:
			out = out + c

	return out

def traceit(frame, event, arg):
	if event == "line":
		filename = frame.f_code.co_filename
		lineno = frame.f_lineno
		line = linecache.getline(filename, lineno)
		print line,

	return traceit

def test():
	sys.settrace(traceit)
	remove_html_markup('"<b>foo</b>"')
	sys.settrace(None)

test()

