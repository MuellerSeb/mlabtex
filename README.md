mlabtex
=======

mlabtex provides a renderer for latex code in mayavi.

Functions
---------
The following functions are provided

 - `render_latex` -- A renderer for latex-code to produce image files.
 - `mlabtex     ` -- A renderer for latex code in mayavi.
 - `mlabimg     ` -- A renderer for image files in mayavi.

Installation
------------
If you want the latest version, just download the
[code](https://github.com/MuellerSeb/mlabtex/archive/master.zip)
and run the following command from the source code directory:

    pip install -U .

Dependencies
------------
 - [NumPy](http://www.numpy.org)
 - [Mayavi](https://docs.enthought.com/mayavi/mayavi/)

For rendering
-------------
 - [matplotlib](https://matplotlib.org/)
 - [sympy](https://www.sympy.org/)


Example
-------
You can use it like the mlab.surf routine:

    from mayavi import mlab
    from mlabtex import mlabtex

    text = (r'Sebastian M\"uller, ' +
            r'$f(x)=\displaystyle\sum_{n=0}^\infty ' +
            r'f^{(n)}(x_0)\cdot\frac{(x-x_0)^n}{n!}$')
    tex = mlabtex(0., 0., 0.,
                  text,
                  color=(0., 0., 0.),
                  orientation=(30., 0., 0.),
                  dpi=1200)
    mlab.axes()
    mlab.show()

[![Latex in Mayavi][1]][1]

Created May 2018, Copyright Sebastian Mueller 2018


  [1]: https://i.stack.imgur.com/lLF58.png
