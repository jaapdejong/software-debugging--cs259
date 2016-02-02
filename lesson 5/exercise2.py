#!/usr/bin/python 
# Modify `input_command` so that it replays or records
# commands as directed by the `mode` variable
# 

resume = True
command_index = 0
def original_input_command():
    global command_index

    commands = ["open", "save", "quit"]
    command = commands[command_index]
    command_index = command_index + 1
    return command

mode = "REPLAY"
# mode = "RECORD"

if mode == "RECORD":
    saved_commands = []
else:
    saved_commands = ["open", "save", "quit"]

saved_commands = []
def input_command():
    global saved_commands
    if mode == "RECORD":
        command = original_input_command()
        saved_commands.append(command)
#        print '[', command, '] --> ', saved_commands
    else:
        # YOUR CODE HERE
        command = saved_commands.pop(0)
#        print '<', command, '> --> ', saved_commands

    return command

def process(command):
    global resume
    print repr(command)
    if command.startswith('q'):
        resume = False

def test():
    global mode, resume, command_index
    mode = "RECORD"
    resume = True
    while resume:
        command = input_command()
        process(command)
    assert saved_commands == ['open', 'save', 'quit']
    mode = "REPLAY"
    resume = True
    command_index = 0
    # Now, replay the saved_commands
    # This should print "open", "save", "quit"
    while resume:
        command = input_command()
        process(command)

test()
