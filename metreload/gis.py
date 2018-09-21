"""
Module for various GIS tasks

author: Erkka Rinne <erkka.rinne@vtt.fi>
"""

import shapefile


def get_shapefile_bbox(file_path):
    """Get the bounding box (extents) of a shapefile layer

    Returns
    -------
    bbox : tuple
        Bounding as (west, east, south, north)

    Raises
    ------
    RuntimeError

    """
    try:
        sf = shapefile.Reader(file_path)
    except shapefile.ShapefileException as err:
        raise RuntimeError(err)
 
    return tuple([sf.bbox[3], sf.bbox[0], sf.bbox[1], sf.bbox[2]])

