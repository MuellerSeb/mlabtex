# -*- coding: utf-8 -*-
"""
Purpose
=======

mlabtex provides a renderer for latex code in mayavi.

Functions
---------
The following functions are provided:

.. autosummary::

   render_latex
   mlabtex
   mlabimg

---
"""
from __future__ import absolute_import

from mlabtex._version import __version__
from mlabtex.core import mlabtex, render_latex, mlabimg


__all__ = ["mlabtex", "render_latex", "mlabimg"]
__all__ += ["__version__"]
