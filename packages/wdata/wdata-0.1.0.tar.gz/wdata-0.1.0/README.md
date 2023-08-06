===============
 W-data Format
===============
This project contains tools for working with and manipulating the
W-data format used for analyzing superfluid data.

This format was originally derived from the W-SLDA project led by
Gabriel Wlazlowski as documented here:

http://git2.if.pw.edu.pl/gabrielw/cold-atoms/wikis/W-data-format

Here we augment this format slightly to facilitate working with
Python.

Generalizations
===============
The original format required a `.wtxt` file with lots of relevant
information.  Here we generalize the format to allow this information
to be specified in the data files, which we allow to be in the NPY
format.
