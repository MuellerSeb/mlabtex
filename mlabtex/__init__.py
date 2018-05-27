# -*- coding: utf-8 -*-
"""
=======
mlabtex
=======

Contents
--------
mlabtex provides a renderer for latex code in mayavi.

Functions
---------
The following functions are provided:

.. autosummary::

   render_latex
   mlabtex
   mlabimg
"""
from __future__ import absolute_import

from mlabtex.core import mlabtex, render_latex, mlabimg

__all__ = ["mlabtex", "render_latex", "mlabimg"]

__version__ = '0.1.1'
