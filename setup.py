# -*- coding: utf-8 -*-
"""
mlabtex
=======

mlabtex provides a rederer for latex code in mayavi.

latex is rendered either by the aid of sympy and latex/dvipng or
by matplotlib. Matplotlib is the fallback case.

by Sebastian Mueller 2018
"""
from setuptools import setup, find_packages
from mlabtex import __version__ as VERSION

DOCLINES = __doc__.split("\n")
README = open("README.md").read()
CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: End Users/Desktop
Intended Audience :: Science/Research
License :: OSI Approved :: \
GNU Lesser General Public License v3 or later (LGPLv3+)
Natural Language :: English
Operating System :: MacOS
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Topic :: Software Development
Topic :: Utilities
"""

setup(
    name="mlabtex",
    version=VERSION,
    maintainer="Sebastian Mueller",
    maintainer_email="sebastian.mueller@ufz.de",
    description=DOCLINES[0],
    long_description=README,
    long_description_content_type="text/markdown",
    author="Sebastian Mueller",
    author_email="sebastian.mueller@ufz.de",
    url="https://github.com/MuellerSeb/mlabtex",
    license="LGPL -  see LICENSE",
    classifiers=[_f for _f in CLASSIFIERS.split("\n") if _f],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    include_package_data=True,
    install_requires=["numpy >= 1.10.0", "mayavi >= 4.5.0"],
    packages=find_packages(exclude=["tests*", "docs*"]),
)
