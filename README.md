mlabtex
=======

mlabtex provides a renderer for latex code in mayavi.

Functions
---------
The following functions are provided

 - `render_latex` -- A renderer for latex-code to produce image files.
 - `mlabtex     ` -- A renderer for latex code in mayavi.

Installation
------------
If you want the latest version, just download the
[code](https://github.com/MuellerSeb/mlabtex/archive/master.zip)
and run the following command from the source code directory:

    pip install -U .

Dependencies
------------
 - [NumPy](http://www.numpy.org)
 - mayavi
 - matplotlib
 - six

Example
-------
    import os
    os.environ['QT_API'] = 'pyqt'
    os.environ['ETS_TOOLKIT'] = 'qt4'
    from mayavi import mlab
    from mlabtex import mlabtex, render_latex

    TEXT = (r'Sebastian M\"uller, ' +
            r'$f(x)=\displaystyle\sum_{n=0}^\infty ' +
            r'f^{(n)}(x_0)\cdot\frac{(x-x_0)^n}{n!}$')

    render_latex(TEXT,
                 path="out.png",
                 color=(0, 0, 0))

    tex = mlabtex(0., 0., 0.,
                  TEXT,
                  color=(0., 0., 0.),
                  orientation=(30., 0., 0.),
                  dpi=1200)
    mlab.axes()
    mlab.show()

Created May 2018, Copyright Sebastian Mueller 2018
