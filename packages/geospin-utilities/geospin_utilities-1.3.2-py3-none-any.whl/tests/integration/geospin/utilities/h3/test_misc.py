try:
    import h3

    h3.k_ring('841e265ffffffff', 4)
except AttributeError:
    from h3 import h3

import geospin.utilities.h3.misc as misc


def test_get_geojson_dict_of_hex_id_boundary():
    hex_id = '871faec4dffffff'
    actual = misc.get_geojson_dict_of_hex_id_boundary(hex_id)

    # Boundary polygon contains 7 points?
    assert len(actual['coordinates'][0]) == 7

    # Dictionary has the desired keys?
    assert ["type", "coordinates"] == list(actual.keys())
