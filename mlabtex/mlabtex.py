# -*- coding: utf-8 -*-
'''
mlabtex - A latex renderer for mayavi
'''
from __future__ import absolute_import, division, print_function

import tempfile
from six import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
from tvtk.api import tvtk


def rot_x(angle, x, y, z, base=(0., 0., 0.)):
    '''
    Rotation around the x-axis to a given base-point.

    Parameter
    ---------
    angle : float
        Angle given in rad.
    x : float
        x components of the points.
    y : float
        y components of the points.
    z : float
        z components of the points.
    base : tuple, optional
        Base point. Default: ``(0, 0, 0)``
    '''
    x_new = x
    y_new = np.cos(angle)*(y-base[1]) - np.sin(angle)*(z-base[2]) + base[1]
    z_new = np.sin(angle)*(y-base[1]) + np.cos(angle)*(z-base[2]) + base[2]

    return x_new, y_new, z_new


def rot_y(angle, x, y, z, base=(0., 0., 0.)):
    '''
    Rotation around the y-axis to a given base-point.

    Parameter
    ---------
    angle : float
        Angle given in rad.
    x : float
        x components of the points.
    y : float
        y components of the points.
    z : float
        z components of the points.
    base : tuple, optional
        Base point. Default: ``(0, 0, 0)``
    '''
    x_new = np.cos(angle)*(x-base[0]) + np.sin(angle)*(z-base[2]) + base[0]
    y_new = y
    z_new = -np.sin(angle)*(x-base[0]) + np.cos(angle)*(z-base[2]) + base[2]

    return x_new, y_new, z_new


def rot_z(angle, x, y, z, base=(0., 0., 0.)):
    '''
    Rotation around the z-axis to a given base-point.

    Parameter
    ---------
    angle : float
        Angle given in rad.
    x : float
        x components of the points.
    y : float
        y components of the points.
    z : float
        z components of the points.
    base : tuple, optional
        Base point. Default: ``(0, 0, 0)``
    '''
    x_new = np.cos(angle)*(x-base[0]) - np.sin(angle)*(y-base[1]) + base[0]
    y_new = np.sin(angle)*(x-base[0]) + np.cos(angle)*(y-base[1]) + base[1]
    z_new = z

    return x_new, y_new, z_new


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
    buf = BytesIO()
    fig.savefig(buf, dpi=dpi,
                transparent=True,
                format=output,
                bbox_inches='tight',
                pad_inches=0.025)
    plt.close(fig)
    with open(path, 'wb') as im_file:
        im_file.write(buf.getvalue())


def mlabtex(x, y, z, text,
            color=(0, 0, 0),
            figure=None,
            name=None,
            opacity=1.0,
            orientation=(0., 0., 0.),
            scale=1.0,
            dpi=1200):
    '''
    Render matplotlib like text in mayavi. Analogous to mlab.text3d.

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
    kwargs = {}
    if figure is not None:
        kwargs["figure"] = figure
    if name is not None:
        kwargs["name"] = name
    # create temporary file for the reference height of the letter "I"
    reffile = tempfile.NamedTemporaryFile(suffix=".png")
    render_latex(r"I",
                 path=reffile.name,
                 dpi=dpi)
    ref = tvtk.PNGReader()
    ref.file_name = reffile.name
    ref.update()
    # Reference heigth of the letter "I"
    ref_y = ref.data_extent[3]
    reffile.close()
    # create temporary file for the png
    pngfile = tempfile.NamedTemporaryFile(suffix=".png")
    # create png file containing text with matplotlib
    render_latex(text,
                 path=pngfile.name,
                 color=color,
                 dpi=dpi)
    # loading image with tvtk
    img = tvtk.PNGReader()
    img.file_name = pngfile.name
    img.update()
    dim = img.data_extent
    dim_x = dim[1]
    dim_y = dim[3]
    # create the texture from the image
    texture = tvtk.Texture(input_connection=img.output_port, interpolate=1)
    pngfile.close()
    # create the surface points
    surfx, surfy = np.mgrid[0:dim_x+1, 0:dim_y+1]*scale/ref_y
    surfx += x
    surfy += y
    surfz = z*np.ones_like(surfx)
    # calculate the angles for rotation
    rad_x = orientation[0]*np.pi/180.
    rad_y = orientation[1]*np.pi/180.
    rad_z = orientation[2]*np.pi/180.
    # rotate the surface according to the orientation
    surfx, surfy, surfz = rot_x(rad_x, surfx, surfy, surfz, (x, y, z))
    surfx, surfy, surfz = rot_y(rad_y, surfx, surfy, surfz, (x, y, z))
    surfx, surfy, surfz = rot_z(rad_z, surfx, surfy, surfz, (x, y, z))
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
    surf.module_manager.scalar_lut_manager.lut.nan_color = (0, 0, 0, 0)

    return surf
