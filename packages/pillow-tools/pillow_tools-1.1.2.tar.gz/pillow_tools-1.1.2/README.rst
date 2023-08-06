pillow-tools
===============
A collection of useful tools for python pillow and ffmpy.

Install
=======

::

    pip install pillow-tools

Create a thumbnail
==================

You can create a smaller version of an image (including .gif) while maintaining the aspect ratio.

::

    from pillow_tools import OptimizeToSize

    imagePath = '/dir/image.png'
    thumbPath = OptimizeToSize(imagePath, maxWidth=1280, maxHeight=720)
    # The thumbPath image is now in the same directory as imagePath.
    # This will scale the image to a new resolution not exceeding the maxWidth/maxHeight but preserving the aspect ratio

    print('thumbPath=', thumbPath)

Output

::

    >>> thumbPath= '/dir/image_1280x720.png'