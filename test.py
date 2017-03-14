import random
import unittest

from hypothesis import example
from hypothesis import given
from hypothesis.strategies import text

import bf2py
import brainfuck


class CompilerTest(unittest.TestCase):
    @given(text(alphabet='<>-+[],.'))
    @example('++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.')
    def test_equivalence(self, program):
        """Sometimes this gets into infinite loops.  Not sure what to
        do about that - valid (and even sane) programs might loop
        forever - e.g. daemons.  Hypothesis supports timing out a test,
        but needs an example to finish.  I.e., it won't kill a running
        infinite-looping example.
        """
        state = random.getstate()
        inputter = '(lambda: [chr(random.randrange(256))])'
        outputter = 'io.StringIO("")'
        python = bf2py.main(program, inputter, outputter)

        exec(python)
        executed_python = locals()['output_stream'].read()

        random.setstate(state)
        executed_bf = brainfuck.execute(program, eval(inputter), eval(outputter)).read()
        self.assertEqual(executed_python, executed_bf)
        random.setstate(state)


if __name__ == '__main__':
    unittest.main()
