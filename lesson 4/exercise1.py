#!/usr/bin/python
# Simple debugger
# See instructions around line 34
import sys
import readline

# Our buggy program
def remove_html_markup(s):
	tag   = False
	quote = False
	startQuote = ""
	out   = ""

	for c in s:
		if c == '<' and not quote:
			tag = True
		elif c == '>' and not quote:
			tag = False
		elif (c == '"' or c == "'") and tag:
			if not quote:
				startQuote = c
				quote = True
			elif c == startQuote:
				startQuote = ""
				quote = False
		elif not tag:
			out = out + c

	return out

print remove_html_markup('xyz')
print remove_html_markup('"<b>foo</b>"')
print remove_html_markup("'<b>foo</b>'")
print remove_html_markup("<a href=\"don't\">link</a>")


