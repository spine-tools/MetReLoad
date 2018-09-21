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
        sfp = shapefile.Reader(file_path)
    except shapefile.ShapefileException as err:
        raise RuntimeError(err)

    return tuple([sfp.bbox[3], sfp.bbox[0],
                  sfp.bbox[1], sfp.bbox[2]])
