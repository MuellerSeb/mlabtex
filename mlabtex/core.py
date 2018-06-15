# -*- coding: utf-8 -*-
'''
mlabtex - A latex renderer for mayavi
'''
from __future__ import absolute_import, division, print_function

import os
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
from tvtk.api import tvtk


IMREAD = {'bmp': tvtk.BMPReader,
          'jpg': tvtk.JPEGReader,
          'jpeg': tvtk.JPEGReader,
          'png': tvtk.PNGReader,
          'pnm': tvtk.PNMReader,
          'dcm': tvtk.DICOMImageReader,
          'tiff': tvtk.TIFFReader,
          'ximg': tvtk.GESignaReader,
          'dem': tvtk.DEMReader,
          'mha': tvtk.MetaImageReader,
          'mhd': tvtk.MetaImageReader,
          'mnc': tvtk.MINCImageReader}


def render_latex(text, path, color=(0, 0, 0), dpi=1200, output='png'):
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
    """
    plt.rc('text', usetex=True)
    fig = plt.figure(figsize=(0.001, 0.001))
    fig.text(0, 0, u'{}'.format(text), fontsize=6, color=color)
    fig.savefig(path, dpi=dpi,
                transparent=True,
                format=output,
                bbox_inches='tight',
                pad_inches=0.02)
    plt.close(fig)


def mlabimg(x, y, z, path,
            figure=None,
            name=None,
            opacity=1.0,
            orientation=(0., 0., 0.),
            scale=1.0,
            typ=None,
            ref_y_extent=None):
    '''
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
    '''
    if typ is None:
        typ = os.path.splitext(path)[1][1:]
    if typ not in IMREAD:
        raise ValueError("The file type is not supported: "+str(typ))
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
    surfx, surfy = np.mgrid[0:dim_x+1, 0:dim_y+1]*scale/ref_y_extent
    surfz = np.zeros_like(surfx)
    # create the surface
    surf = mlab.surf(surfx, surfy, surfz,
                     color=(1, 1, 1),
                     opacity=opacity,
                     warp_scale=1.,
                     reset_zoom=False,
                     **kwargs)
    # add the texture
    surf.actor.enable_texture = True
    surf.actor.tcoord_generator_mode = 'plane'
    surf.actor.actor.texture = texture
    surf.actor.actor.orientation = orientation
    surf.actor.actor.position = (x, y, z)

    return surf


def mlabtex(x, y, z, text,
            color=(0, 0, 0),
            figure=None,
            name=None,
            opacity=1.0,
            orientation=(0., 0., 0.),
            scale=1.0,
            dpi=1200):
    '''
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
    '''
    # create temporary file for the reference height of the letter "I"
    reffile = tempfile.NamedTemporaryFile(suffix=".png")
    render_latex(r"I", path=reffile.name, dpi=dpi)
    ref = tvtk.PNGReader()
    ref.file_name = reffile.name
    ref.update()
    # Reference heigth of the letter "I"
    ref_y = ref.data_extent[3]
    reffile.close()
    # create temporary file for the png
    pngfile = tempfile.NamedTemporaryFile(suffix=".png")
    # create png file containing text with matplotlib
    render_latex(text, path=pngfile.name, color=color, dpi=dpi)
    # loading image with tvtk
    surf = mlabimg(x, y, z, pngfile.name,
                   figure, name, opacity, orientation, scale,
                   typ="png", ref_y_extent=ref_y)
    # close temp file
    pngfile.close()

    return surf
