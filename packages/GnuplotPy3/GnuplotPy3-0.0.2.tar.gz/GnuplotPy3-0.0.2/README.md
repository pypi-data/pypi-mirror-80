[`Gnuplot-py`](http://gnuplot-py.sourceforge.net/) written by Michael Haggerty
`<mhagger@alum.mit.edu>` is an amazing Python2 package which allows a Python
user to incoporate any Gnuplot command within a Python2 script.  However,
Python2 has ended its update in the year of 2020.  A Python3 solution will
be appreciated.  

This module only does one job -- it allows calling any Gnuplot command in a
Python3 script.  Please refer to the example below for a quick start.

```
import GnuplotPy3
gp = GnuplotPy3.GnuplotPy3()
gp('set terminal postscript eps size 3.5, 2.62 \\'     )
gp('                            enhanced color \\'     )
gp("                            font 'Helvetica,14' \\")
gp('                            linewidth 2'           )
gp("set output 'sinx.eps'")
gp("unset key")
gp("plot sin(x)")
```
