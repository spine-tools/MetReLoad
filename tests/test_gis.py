import os.path

from numpy import isclose

from metreload.gis import get_shapefile_bbox


def test_bbox(datadir):
    assert isclose(get_shapefile_bbox(os.path.join(datadir, 'areas.shp')),
                   (-7.784538191975432, 13.428893993210842,
                    -9.59606517346118,   2.225849462962977)).all()
    