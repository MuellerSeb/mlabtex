# mlabtex

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3380567.svg)](https://doi.org/10.5281/zenodo.3380567)
[![PyPI version](https://badge.fury.io/py/mlabtex.svg)](https://badge.fury.io/py/mlabtex)
[![Build Status](https://travis-ci.org/MuellerSeb/mlabtex.svg?branch=master)](https://travis-ci.org/MuellerSeb/mlabtex)
[![Coverage Status](https://coveralls.io/repos/github/MuellerSeb/mlabtex/badge.svg?branch=master)](https://coveralls.io/github/MuellerSeb/mlabtex?branch=master)
[![Documentation Status](https://readthedocs.org/projects/mlabtex/badge/?version=latest)](https://mlabtex.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Purpose

mlabtex provides a renderer for latex code in mayavi.


## Installation

    pip install mlabtex


## Functions

The following functions are provided

 - `render_latex` -- A renderer for latex-code to produce image files.
 - `mlabtex     ` -- A renderer for latex code in mayavi.
 - `mlabimg     ` -- A renderer for image files in mayavi.


## Dependencies

 - [NumPy](http://www.numpy.org)
 - [Mayavi](https://docs.enthought.com/mayavi/mayavi/)


### For rendering

 - [matplotlib](https://matplotlib.org/)
 - [sympy](https://www.sympy.org/)


## Example

You can use it like the mlab.surf routine:

    from mayavi import mlab
    from mlabtex import mlabtex

    text = (
        r'Sebastian M\"uller, '
        + r'$f(x)=\displaystyle\sum_{n=0}^\infty '
        + r'f^{(n)}(x_0)\cdot\frac{(x-x_0)^n}{n!}$'
    )
    tex = mlabtex(
        0., 0., 0.,
        text,
        color=(0., 0., 0.),
        orientation=(30., 0., 0.),
        dpi=1200,
    )
    mlab.axes()
    mlab.show()

[![Latex in Mayavi][1]][1]

Copyright Sebastian Mueller 2019


  [1]: https://i.stack.imgur.com/lLF58.png
