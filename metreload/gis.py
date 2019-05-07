###############################################################################
# Copyright (C) 2018–2019  The Spine Project Authors
#
# This file is part of MetReload
#
# MetReLoad is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

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
