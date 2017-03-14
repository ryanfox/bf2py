# taken from https://github.com/ryanfox/brainfuck/releases/tag/v0.0.1

import re
import sys

from collections import defaultdict


def brackets_are_balanced(bf):
    if bf.count('[') != bf.count(']'):
        return False

    depth = 0
    for symbol in bf:
        if symbol == '[':
            depth += 1
        elif symbol == ']':
            depth -= 1
        if depth < 0:
            return False
    return True


def execute(commands, input_stream=input, output_stream=sys.stdout):
    """
    commands is a string containing the brainfuck program.
    input_stream is a callable, which provides one byte of input when called
    """
    if not brackets_are_balanced(commands):
        return output_stream

    cells = defaultdict(int)
    cellptr = 0
    codeptr = 0
    
    # scan to match [ and ]
    loops = []
    opens = {}
    closes = {}
    while codeptr < len(commands):
        if commands[codeptr] == '[':
            loops.append(codeptr)
        elif commands[codeptr] == ']':
            start = loops.pop()
            opens[start] = codeptr
            closes[codeptr] = start
        codeptr += 1


    # reset code pointer and actually run program
    codeptr = 0    
    while codeptr < len(commands):
        if commands[codeptr] == '+':
            cells[cellptr] += 1
        elif commands[codeptr] == '-':
            cells[cellptr] -= 1
        elif commands[codeptr] == '<':
            cellptr -= 1
        elif commands[codeptr] == '>':
            cellptr += 1
        elif commands[codeptr] == ',':
            cells[cellptr] = ord(input_stream()[0])
        elif commands[codeptr] == '.':
            print(chr(cells[cellptr] % 256), end='', file=output_stream),
        elif commands[codeptr] == '[':
            if cells[cellptr] == 0:
                codeptr = opens[codeptr]
        elif commands[codeptr] == ']':
            if cells[cellptr] != 0:
                codeptr = closes[codeptr]
        codeptr += 1

    return output_stream


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python brainfuck.py <input.b>')
        sys.exit(1)
    with open(sys.argv[1]) as f:
        program = f.read()
        filtered = re.sub('[^+-[],.<>]', '', program)
        commands = list(filtered)
        execute(commands)
