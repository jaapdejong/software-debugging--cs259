#!/usr/bin/env python
# Compute line coverage
import sys
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""
    for c in s:
        # print c, tag, quote
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    # assert out.find('<') == -1
    return out
    
coverage = {}

def traceit(frame, event, arg):
    global coverage

    if event == "line":
        filename = frame.f_code.co_filename
        lineno   = frame.f_lineno
        if not coverage.has_key(filename):
            coverage[filename] = {}
        coverage[filename][lineno] = True
        
    return traceit
    
def print_coverage(coverage, covered_file = None):
#    print coverage
    for filename in coverage.keys():
#        print coverage[filename]
        if covered_file is not None:
            lines = covered_file.splitlines(True)
        else:
            lines = open(filename).readlines()
        # YOUR CODE HERE
        # PRINT EACH COVERED LINE WITH A PREFIX OF "* "
        # AND EACH UNCOVERED WITH A PREFIX OF "  "
        lineno = 1
        for line in lines:
            if lineno in coverage[filename]:
                print '*',
            else:
                print ' ',
            print line,
            lineno += 1

sys.settrace(traceit)

remove_html_markup('foo')          # 1
remove_html_markup('<b>foo</b>')   # 2
remove_html_markup('"<b>foo</b>"') # 3
#print coverage
#{'./exercise4.py': {5: True, 6: True, 7: True, 8: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True, 17: True, 19: True}}

sys.settrace(None)

c_file = """#!/usr/bin/env python
# Compute line coverage
import sys
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""
    for c in s:
        # print c, tag, quote
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    # assert out.find('<') == -1
    return out
"""

print_coverage(coverage, c_file)
#print_coverage(coverage)
