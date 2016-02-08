#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# The provided code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the provided code
# to work also on function calls (you can use your code from problem set 5 here)
# Use the mystery function that can be found at line 170 and the
# test cases at line 165 for this exercise.
# Remember that for functions the phi values have to be calculated as
# described in the problem set 5 video - 
# you should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
#
# Then combine both approaches to find out the function call and its return
# value that is the most correlated with failure, and then - the line in the
# function. Calculate phi values for the function and the line and put them
# in the variables below. 
# Do NOT set these values dynamically.

answer_function = "f2"   # One of f1, f2, f3
answer_bin = -1          # One of 1, 0, -1
answer_function_phi = 0.6547  # precision to 4 decimal places.
answer_line_phi = 0.6547      # precision to 4 decimal places.
# if there are several lines with the same phi value, put them in a list,
# no leading whitespace is required
answer_line = ['return "FAIL"', 'return "FAIL"', 'elif other < 1:', 'grade -= 1']  # lines of code

# the correct values according to udacity are:
answer_line_phi = 1.0000      # precision to 4 decimal places.
answer_line = ['elif other < 1:', 'grade -= 1']  # lines of code

# answer_line_phi and answer_line are from the list below
# there must be an error in it...
####	### Lines ###
#### >>	+0.6547 1 0 1 6         return "FAIL"
####	-0.6547 1 6 1 0     elif (r1 + r2 + r3) < 0:
#### >>	+0.6547 1 0 1 6         return "FAIL"
####	-1.0000 0 6 2 0     elif r1 == 0 and r2 == 0:
####	-1.0000 0 6 2 0         return "PASS"
####	-0.3333 0 2 2 4         return 1
####	+0.3333 2 4 0 2         return 0
####	+0.2182 2 5 0 1         elif c.isalpha():
####	+0.3333 2 4 0 2             letters += 1
####	-0.6547 1 6 1 0         grade += 1 
#### >>	+0.6547 1 0 1 6     elif other < 1:
#### >>	+0.6547 1 0 1 6         grade -= 1
####	+0.3333 1 1 1 5             grade -= 1
####	-0.3333 0 2 2 4         grade += 1

# answer_function, answer_bin and answer_function_phi are from the list below
####	### Functions ###
####	+0.3333 2 4 0 2 f1 0
####	-0.3333 0 2 2 4 f1 1
#### >>	+0.6547 1 0 1 6 f2 -1
####	-0.6547 1 6 1 0 f2 1
#### >>	+0.6547 1 0 1 6 f3 -1
####	-0.3333 1 5 1 1 f3 0
####	-0.2182 0 1 2 5 f3 1


# The buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:

        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out

# global variable to keep the coverage data in
coverage = {}
coverageFunctions = {}
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in 
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        coverage[lineno] = True

    elif event == "return":
        functionName = frame.f_code.co_name
        if arg < 0: bin = -1
        elif arg > 0: bin = 1
        else: bin = 0
        coverageFunctions[functionName] = bin
        
    return traceit

# Calculate phi coefficient from given values            
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) / 
             math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each covered line
def print_tables(tables):
    lines = open("exercise4.py").readlines()
    oline = None
    for line in tables:
        if oline == None: oline = line
        else: oline += 1
        while oline < line:
            print "                #%3d" % oline, lines[oline - 1],
            oline += 1
        (n11, n10, n01, n00) = tables[line]
        try:
            factor = phi(n11, n10, n01, n00)
            prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
        except:
            prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
                
        print prefix, "#%3d" % line, lines[line - 1],

# Run the program with each test case and record 
# input, outcome and coverage of lines
def run_tests(inputs):
    global coverage
    global coverageFunctions

    runs = []
    runsFunctions = []
    for input in inputs:
        coverage = {}
        coverageFunctions = {}
        sys.settrace(traceit)
        outcome = mystery(input)
        sys.settrace(None)
        runs.append((input, outcome, coverage))
        runsFunctions.append((input, outcome, coverageFunctions))
    return runs, runsFunctions

# Create empty tuples for each covered line
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for line in coverage:
            tables[line] = (0, 0, 0, 0)
    return tables

# Compute n11, n10, etc. for each line
def compute_n(tables):
    for line in tables:
        (n11, n10, n01, n00) = tables[line]
        for (input, outcome, coverage) in runs:
            if line in coverage:
                # Covered in this run
                if outcome == "FAIL":
                    n11 += 1  # covered and fails
                else:
                    n10 += 1  # covered and passes
            else:
                # Not covered in this run
                if outcome == "FAIL":
                    n01 += 1  # uncovered and fails
                else:
                    n00 += 1  # uncovered and passes
        tables[line] = (n11, n10, n01, n00)
    return tables

# These are the input values you should test the mystery function with
inputs = ["aaaaa223%", "aaaaaaaatt41@#", "asdfgh123!", "007001007", "143zxc@#$ab", "3214&*#&!(", "qqq1dfjsns", "12345%@afafsaf"]

###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == str
    assert len(magic) > 0
    
    r1 = f1(magic)
    
    r2 = f2(magic)
    
    r3 = f3(magic)
    
    print magic, r1, r2, r3

    if r1 < 0 or r3 < 0:
        return "FAIL"
    elif (r1 + r2 + r3) < 0:
        return "FAIL"
    elif r1 == 0 and r2 == 0:
        return "FAIL"
    else:
        return "PASS"


def f1(ml):
    if len(ml) <6:
        return -1
    elif len(ml) > 12 :
        return 1
    else:
        return 0
    
def f2(ms):
    digits = 0
    letters = 0
    for c in ms:
        if c in "1234567890":
            digits += 1
        elif c.isalpha():
            letters += 1
    other = len(ms) - digits - letters
    grade = 0
    
    if (other + digits) > 3:
        grade += 1 
    elif other < 1:
        grade -= 1
           
    return grade

def f3(mn):
    forbidden = ["pass", "123", "qwe", "111"]
    grade = 0
    for word in forbidden:
        if mn.find(word) > -1:
            grade -= 1
    if mn.find("%") > -1:
        grade += 1
    return grade

# Create empty tuples for each covered line
def init_tablesFunctions(runsFunctions):
    tablesFunctions = {}
    for (input, outcome, coverageFunctions) in runsFunctions:
        for functionName in coverageFunctions:
            for bin in range(-1,2):
                if not functionName in tablesFunctions:
                    tablesFunctions[functionName] = {}
                if not bin in tablesFunctions[functionName]:
                    tablesFunctions[functionName][bin] = (0, 0, 0, 0)

    return tablesFunctions

# Compute n11, n10, etc. for each line
def compute_nFunctions(tablesFunctions):
    for functionName in tablesFunctions:
        bins = tablesFunctions[functionName]
        for bin in range(-1,2):
            (n11, n10, n01, n00) = tablesFunctions[functionName][bin]
            for (input, outcome, coverageFunctions) in runsFunctions:
                if functionName in coverageFunctions and coverageFunctions[functionName] == bin:
                    # Covered in this run
                    if outcome == "FAIL":
                        n11 += 1  # covered and fails
                    else:
                        n10 += 1  # covered and passes
                else:
                    # Not covered in this run
                    if outcome == "FAIL":
                        n01 += 1  # uncovered and fails
                    else:
                        n00 += 1  # uncovered and passes
            tablesFunctions[functionName][bin] = (n11, n10, n01, n00)

    return tablesFunctions

# Print out values of phi, and result of runs for each covered line
def print_tablesFunctions(tablesFunctions):
    for functionName in tablesFunctions:
        for bin in range(-1,2):
            if bin in tablesFunctions[functionName]:
                (n11, n10, n01, n00) = tablesFunctions[functionName][bin]
                try:
                    factor = phi(n11, n10, n01, n00)
                    prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
                    print prefix, functionName, bin
                except:
                    prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
                    
            else:
                prefix = "               "
                    
            #print prefix, functionName, bin

# go ahead!
print "### Run ###"
runs, runsFunctions = run_tests(inputs)
print

print "### Lines ###"
tables = init_tables(runs)
tables = compute_n(tables)
print_tables(tables)
print

print "### Functions ###"
tablesFunctions = init_tablesFunctions(runsFunctions)
tablesFunctions = compute_nFunctions(tablesFunctions)
print_tablesFunctions(tablesFunctions)
print

