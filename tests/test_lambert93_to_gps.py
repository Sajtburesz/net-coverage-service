import pytest
from helpers.lambert93_to_gps import lambert93_to_gps


class TestLambert93ToGps:

    # got the expected using this converter: https://geofree.fr/gf/coordinateconv.asp
    @pytest.mark.parametrize(["x","y","expected"], [
        (700000,6600000, (3.0000000, 46.5000000)),
        (841000, 6519000, (4.8139894, 45.7560252))
    ])
    def test_valid_x_y(self,x, y, expected):
        lon, lat = lambert93_to_gps(x, y)
        assert (round(lon, 7), round(lat, 7)) == expected

    def test_not_int_input(self):
        with pytest.raises(ValueError):
            lambert93_to_gps("alma", 567890)