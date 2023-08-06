#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

class GnuplotPy3:
    def __init__(self):
        # 
        # Real time output requires `stdout = None` and `stderr = None`. 
        # `shell = True` might break the code on non-unix system.  But it 
        # provides flexibility to customize the command, e.g. with arguments.  
        # 
        self.gnuplot = Popen('gnuplot', shell = True, stdin=PIPE)


    def __del__(self):
        # Turn off stdin...
        self.gnuplot.stdin.close()

        # Wait until plotting is over...
        self.gnuplot.wait()

        # Terminate the subprcess...
        self.gnuplot.terminate()


    def __call__(self, s):
        # Keep reading the new Gnuplot command as a byte string...
        self.gnuplot.stdin.write( bytes( (s + '\n').encode() ) )

        # Flush it asap...
        self.gnuplot.stdin.flush()
