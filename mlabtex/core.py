# -*- coding: utf-8 -*-
"""
mlabtex - A latex renderer for mayavi
"""
from __future__ import absolute_import, division, print_function

import os
import tempfile
import numpy as np
from mayavi import mlab
from tvtk.api import tvtk

# all supported image formates by tvtk
IMREAD = {
    "bmp": tvtk.BMPReader,
    "jpg": tvtk.JPEGReader,
    "jpeg": tvtk.JPEGReader,
    "png": tvtk.PNGReader,
    "pnm": tvtk.PNMReader,
    "dcm": tvtk.DICOMImageReader,
    "tiff": tvtk.TIFFReader,
    "ximg": tvtk.GESignaReader,
    "dem": tvtk.DEMReader,
    "mha": tvtk.MetaImageReader,
    "mhd": tvtk.MetaImageReader,
    "mnc": tvtk.MINCImageReader,
}


class RenderError(Exception):
    pass


class TmpFile(object):
    """
    A closed temporary file class

    Attributes
    ----------
    name : string
        Name and path to the file.
    file : class
        Temporary file handler
    """

    def __init__(self, suffix="txt"):
        """
        A closed temporary file

        Parameter
        ---------
        suffix : string, optional
            The suffix for the temporary file. Default: "txt"
        """
        self.file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        self.file.close()

    @property
    def name(self):
        return self.file.name

    def close(self):
        os.unlink(self.name)


def render_latex_mpl(text, path, color=(0, 0, 0), dpi=600, output="png"):
    """
    Renders LaTeX-formula into an image with matplotlib.

    Parameters
    ----------
    text : string
        String containing the latex-code.
    path : string
        Path to the file to be saved.
    color : tuple, optional
        color of the text given as rgb tuple. Default: ``(0, 0, 0)``
    dpi : int, optional
        Used dpi. Default: 1200
    output : string, optional
        Output format. Default: ``"png"``

    Notes
    -----
    If you get the following error:

        ``RuntimeError: libpng signaled error``

    Try to set the dpi higher. (1200 recomended)

    If big symbols like ``\\int`` or ``\\sum`` don't show up properly,
    try setting a

        ``\\displaystyle``

    infront of them.
    """
    from matplotlib.mathtext import MathTextParser
    from matplotlib.font_manager import FontProperties
    from matplotlib import figure, rc

    # backend_agg supports all of the core output formats
    from matplotlib.backends import backend_agg

    rc("text", usetex=False)
    prop = FontProperties()
    parser = MathTextParser("path")
    width, height, depth, _, _ = parser.parse(text, dpi=72, prop=prop)
    fig = figure.Figure(figsize=(width / 72.0, height / 72.0))
    fig.text(0, depth / height, text, fontproperties=prop, color=color)
    backend_agg.FigureCanvasAgg(fig)
    fig.savefig(path, dpi=dpi, format=output, transparent=True)


def render_latex_sympy(text, path, color=(0, 0, 0), dpi=600, output="png"):
    """
    Renders LaTeX-formula into an image with sympy.

    Parameters
    ----------
    text : string
        String containing the latex-code.
    path : string
        Path to the file to be saved.
    color : tuple, optional
        color of the text given as rgb tuple. Default: ``(0, 0, 0)``
    dpi : int, optional
        Used dpi. Default: 1200
    output : string, optional
        Output format. Default: ``"png"``

    Notes
    -----
    If you get the following error:

        ``RuntimeError: libpng signaled error``

    Try to set the dpi higher. (1200 recomended)

    If big symbols like ``\\int`` or ``\\sum`` don't show up properly,
    try setting a

        ``\\displaystyle``

    infront of them.
    """
    from sympy import preview

    preamble = (
        r"\documentclass[12pt]{article}"
        + os.linesep
        + r"\pagestyle{empty}"
        + os.linesep
        + r"\usepackage[utf8]{inputenc}"
        + os.linesep
        + r"\usepackage{amsmath}"
        + os.linesep
        + r"\usepackage{amsfonts}"
        + os.linesep
        + r"\usepackage{helvet}"
        + os.linesep
        + r"\renewcommand{\familydefault}{\sfdefault}"
        + os.linesep
        + r"\usepackage{xcolor}"
        + os.linesep
        + r"\definecolor{user}{rgb}"
        + "{"
        + "{}, {}, {}".format(*color)
        + "}"
        + os.linesep
        + r"\color{user}"
        + os.linesep
        + r"\everymath{\displaystyle}"
        + os.linesep
        + r"\begin{document}"
    )
    preview(
        text,
        viewer="file",
        output=output,
        filename=path,
        preamble=preamble,
        euler=False,
        dvioptions=[
            "-T",
            "tight",
            "-z",
            "0",
            "--truecolor",
            "-D",
            str(int(dpi)),
            "-bg",
            "Transparent",
        ],
    )


def render_latex(text, path, color=(0, 0, 0), dpi=600, output="png"):
    """
    Renders LaTeX-formula into an image.

    Parameters
    ----------
    text : string
        String containing the latex-code.
    path : string
        Path to the file to be saved.
    color : tuple, optional
        color of the text given as rgb tuple. Default: ``(0, 0, 0)``
    dpi : int, optional
        Used dpi. Default: 1200
    output : string, optional
        Output format. Default: ``"png"``

    Notes
    -----
    If you get the following error:

        ``RuntimeError: libpng signaled error``

    Try to set the dpi higher. (1200 recomended)

    If big symbols like ``\\int`` or ``\\sum`` don't show up properly,
    try setting a

        ``\\displaystyle``

    infront of them.

    It will try to render it with sympy first.
    If that fails it will use matplotlib.
    """
    try:
        render_latex_sympy(text, path, color, dpi, output)
    except Exception as exc_1:
        try:
            render_latex_mpl(text, path, color, dpi, output)
        except Exception as exc_2:
            raise RenderError(
                "Mlabtex: Could not render the latex-code..."
                + os.linesep
                + str(exc_1)
                + os.linesep
                + str(exc_2)
                + os.linesep
            )


def mlabimg(
    x,
    y,
    z,
    path,
    figure=None,
    name=None,
    opacity=1.0,
    orientation=(0.0, 0.0, 0.0),
    scale=1.0,
    typ=None,
    ref_y_extent=None,
):
    """
    Render image files in mayavi. Analogous to mlab.text3d.

    Parameter
    ---------
    x : float
        x position of the text.
    y : float
        y position of the text.
    z : float
        z position of the text.
    path : string
        Path to the image file.
    color : tuple, optional
        color of the text given as rgb tuple. Default: ``(0, 0, 0)``
    figure : Scene, optional
        Must be a Scene or None.
    name : string, optional
        the name of the vtk object created.
    opacity : float, optional
        The overall opacity of the vtk object. Must be a float. Default: 1.0
    orientation : tuple, optional
        the angles giving the orientation of the text.
        If the text is oriented to the camera,
        these angles are referenced to the axis of the camera.
        If not, these angles are referenced to the z axis.
        Must be an array with shape (3,).
    scale : float, optional
        The vetical scale of the image, in figure units.
    typ : string, optional
        Here you can specify the image type. Supported:
        'bmp', 'jpg', 'jpeg', 'png', 'pnm', 'dcm', 'tiff', 'ximg', 'dem',
        'mha', 'mhd', 'mnc'.
        If set to ``None``, the file type is determined by its extension.
        Default: None.
    ref_y_extent : int, optional
        Reference vertical extent of the image to scale to.
        If set to ``None``, the image extent itself is used. Default: None

    Return
    ------
    surf : Surf
        Mayavi ``Surf`` class with the rendered image as texture.
    """
    if typ is None:
        typ = os.path.splitext(path)[1][1:].lower()
    if typ not in IMREAD:
        raise ValueError("The file type is not supported: " + str(typ))
    reader = IMREAD[typ]
    kwargs = {}
    if figure is not None:
        kwargs["figure"] = figure
    if name is not None:
        kwargs["name"] = name
    # load the image
    img = reader()
    img.file_name = path
    img.update()
    dim_x, dim_y = img.data_extent[1:4:2]
    # create the texture from the image
    texture = tvtk.Texture(input_connection=img.output_port, interpolate=0)
    # create the surface points
    if ref_y_extent is None:
        ref_y_extent = dim_y
    surfx, surfy = np.mgrid[0 : dim_x + 1, 0 : dim_y + 1] * scale / ref_y_extent
    surfz = np.zeros_like(surfx)
    # create the surface
    surf = mlab.surf(
        surfx,
        surfy,
        surfz,
        color=(1, 1, 1),
        opacity=opacity,
        warp_scale=1.0,
        reset_zoom=False,
        **kwargs
    )
    # add texture, position and orientation
    surf.actor.enable_texture = True
    surf.actor.tcoord_generator_mode = "plane"
    surf.actor.actor.texture = texture
    surf.actor.actor.orientation = orientation
    surf.actor.actor.position = (x, y, z)

    return surf


def mlabtex(
    x,
    y,
    z,
    text,
    color=(0, 0, 0),
    figure=None,
    name=None,
    opacity=1.0,
    orientation=(0.0, 0.0, 0.0),
    scale=1.0,
    dpi=1200,
):
    """
    Render for matplotlib like text in mayavi. Analogous to mlab.text3d.

    Parameter
    ---------
    x : float
        x position of the text.
    y : float
        y position of the text.
    z : float
        z position of the text.
    text : string
        The text is positionned in 3D, in figure coordinnates.
    color : tuple, optional
        color of the text given as rgb tuple. Default: ``(0, 0, 0)``
    figure : Scene, optional
        Must be a Scene or None.
    name : string, optional
        the name of the vtk object created.
    opacity : float, optional
        The overall opacity of the vtk object. Must be a float. Default: 1.0
    orientation : tuple, optional
        the angles giving the orientation of the text.
        If the text is oriented to the camera,
        these angles are referenced to the axis of the camera.
        If not, these angles are referenced to the z axis.
        Must be an array with shape (3,).
    scale : float, optional
        The scale of the text, in figure units. It is rescaled by the size of
        the letter "I".
    dpi : int, optional
        Used dpi. Default: 1200

    Return
    ------
    surf : Surf
        Mayavi ``Surf`` class with the rendered text as texture.

    Notes
    -----
    If you get the following error:

        ``RuntimeError: libpng signaled error``

    Try to set the dpi higher. (1200 recomended)

    If big symbols like ``\\int`` or ``\\sum`` don't show up properly,
    try setting a

        ``\\displaystyle``

    infront of them.
    """
    # create temporary file for the reference height of the letter "I"
    reffile = TmpFile(suffix=".png")
    render_latex(r"I", path=reffile.name, dpi=dpi)
    ref = tvtk.PNGReader()
    ref.file_name = reffile.name
    ref.update()
    # Reference heigth of the letter "I"
    ref_y = ref.data_extent[3]
    reffile.close()
    # create temporary file for the png
    pngfile = TmpFile(suffix=".png")
    # create png file containing text with matplotlib
    render_latex(text, path=pngfile.name, color=color, dpi=dpi)
    # loading image with tvtk
    surf = mlabimg(
        x,
        y,
        z,
        pngfile.name,
        figure,
        name,
        opacity,
        orientation,
        scale,
        typ="png",
        ref_y_extent=ref_y,
    )
    # close temp file
    pngfile.close()

    return surf
