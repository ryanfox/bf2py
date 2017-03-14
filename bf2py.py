# bf2py.py
# a brainfuck-to-python compiler

import re
import sys


def pad(string, depth):
    return (' ' * (depth * 4)) + string


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


def main(bf, input_stream='input', output_stream='sys.stdout'):

    cleaned_bf = re.sub(r'[^<>,.+-[\]]', '', bf)
    python = []

    if brackets_are_balanced(cleaned_bf):

        depth = 0
        for i in range(len(cleaned_bf)):
            symbol = cleaned_bf[i]

            if symbol == '<':
                python.append(pad('i -= 1', depth))
            if symbol == '>':
                python.append(pad('i += 1', depth))
            if symbol == ',':
                python.append(pad('cells[i] = ord(input_stream()[0])', depth))
            if symbol == '.':
                python.append(pad('print(chr(cells[i] % 256), end="", file=output_stream)', depth))
            if symbol == '+':
                python.append(pad('cells[i] += 1', depth))
            if symbol == '-':
                python.append(pad('cells[i] -= 1', depth))
            if symbol == '[':
                python.append(pad('while cells[i] != 0:', depth))
                python.append(pad('pass', depth=depth+1))
                depth += 1
            if symbol == ']':
                depth -= 1

            i += 1

    return '''from collections import defaultdict
import io
import sys

i = 0
cells = defaultdict(int)
input_stream = {}
output_stream = {}

{}
'''.format(input_stream, output_stream, '\n'.join(python))


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        bf = f.read()
    print(main(bf))
