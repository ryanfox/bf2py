# bf2py.py
# a brainfuck-to-python compiler

import re
import sys


def pad(string, depth):
    return (' ' * (depth * 4)) + string


def get_loops(program):
    loops = {}
    for i, symbol in enumerate(program):
        if symbol == '[':
            j = i + 1
            depth = 0
            for candidate in program[j:]:
                if candidate == ']':
                    if depth == 0:
                        loops[i] = j
                        loops[j] = i
                        break
                    else:
                        depth -= 1

                elif candidate == '[':
                    depth += 1

                j += 1

    return loops


with open(sys.argv[1]) as f:
    bf = f.read()

cleaned_bf = re.sub(r'[^<>,.+-[\]]', '', bf)
loops = get_loops(cleaned_bf)

python = []
i = 0
depth = 0
for i in range(len(cleaned_bf)):
    symbol = cleaned_bf[i]

    if symbol == '<':
        python.append(pad('i -= 1', depth))
    if symbol == '>':
        python.append(pad('i += 1', depth))
    if symbol == ',':
        python.append(pad('cells[i] = ord(input()[0])', depth))
    if symbol == '.':
        python.append(pad('print(chr(cells[i]), end=\'\')', depth))
    if symbol == '+':
        python.append(pad('cells[i] += 1', depth))
    if symbol == '-':
        python.append(pad('cells[i] -= 1', depth))
    if symbol == '[':
        python.append(pad('while cells[i] != 0:', depth))
        depth += 1
    if symbol == ']':
        depth -= 1

    i += 1

print('''from collections import defaultdict
i = 0
cells = defaultdict(int)

{}
'''.format('\n'.join(python)))
