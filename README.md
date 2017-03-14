# bf2py
A brainfuck-to-python compiler.

Usage: `python bf2py.py <bf_program.bf> > bf_program.py`


To run the tests:

    $ pip install -r requirements.txt
    $ python test.py

Sometimes the tests hang - it generated an infinite-looping bf program.  Not
much can be done about that right now.  `CTRL + C` kills the tests if so.