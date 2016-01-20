#!/usr/bin/python
# Finish the simplify function.
# Have it deal with the case where test(s1) doesn't fail
# 
# If neither s1 or s2 cause the test to fail then return 
# the original string, s.

import re

def test(s):
	if re.search("<SELECT[^>]*>", s) >= 0:
#		print s, len(s), "FAIL"
		return "FAIL"
	else:
#		print s, len(s), "PASS"
		return "PASS"

def simplify(s):
	assert test(s) == "FAIL"

	print s, len(s)

	split = len(s) / 2
	s1 = s[:split]
	s2 = s[split:]

	if test(s1) == "FAIL":
		return simplify(s1)
	# YOUR CODE HERE
	if test(s2) == "FAIL":
		return simplify(s2)
	return s

# UNCOMMENT TO TEST
html_input = '<SELECT><OPTION VALUE="simplify><OPTION VALUE="beautify"></SELECT>'
#html_input = '<SELECT>foo</SELECT>'
#html_input = '<SELECT>'
print simplify(html_input)

