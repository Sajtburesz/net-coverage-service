import pytest
from helpers.geo_coding_helper import GeoCodingHelper
from helpers.external_adresses import reverse_geocoding, geo_search
from exceptions.GeoCodingExceptions import GeoCodingPointNotFound, GeoCodingMissingCityCodes

class TestGeocodingHelper:
    def setup_method(self):
        self.geocoding_helper = GeoCodingHelper()

    @pytest.mark.parametrize(["lon", "lat"], [
        ("apple", 43.2965),
        (43.2965, "watermelon")
    ])
    def test_not_float_input_gps(self, lon, lat):
        with pytest.raises(AttributeError, match="Longitude or Latitude is not a float."):
            self.geocoding_helper.get_insee_and_post_with_gps(lon, lat)

    def test_not_str_input_address(self):
        with pytest.raises(AttributeError, match="Address is not a string."):
            self.geocoding_helper.get_insee_and_post_with_address(15)

    def test_valid_input_based_on_address(self, mocker, mock_geocoding_response_no_list):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = mock_geocoding_response_no_list
        mock_get.return_value.status_code = 200

        insee, postcode = self.geocoding_helper.get_insee_and_post_with_address("Paris")

        mock_get.assert_called_once_with(geo_search, params={"index": "address, poi", "q": "Paris", "limit": 1})
        assert insee == 75056
        assert postcode == 75001

    def test_valid_input_based_on_gps(self, mocker, mock_geocoding_response_with_list):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = mock_geocoding_response_with_list
        mock_get.return_value.status_code = 200

        insee, postcode = self.geocoding_helper.get_insee_and_post_with_gps(2.3522, 48.8566)

        mock_get.assert_called_once_with(reverse_geocoding, params={"index": "address, poi", "lon": 2.3522, "lat": 48.8566, "limit": 1})
        assert insee == 75056
        assert postcode != 8911123

    def test_no_features_returned(self, mocker, mock_empty_response):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = mock_empty_response
        mock_get.return_value.status_code = 200

        with pytest.raises(GeoCodingPointNotFound, match="No Geocoding Point found."):
            self.geocoding_helper.get_insee_and_post_with_gps(2.3522, 48.8566)

    def test_missing_citycode_and_postcode(self, mocker, mock_missing_codes_response):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = mock_missing_codes_response
        mock_get.return_value.status_code = 200

        with pytest.raises(GeoCodingMissingCityCodes, match="Both insee and postcode are missing."):
            self.geocoding_helper.get_insee_and_post_with_gps(2.3522, 48.8566)

    def test_missing_citycode(self, mocker, mock_missing_citycode_response):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = mock_missing_citycode_response
        mock_get.return_value.status_code = 200

        insee, postcode = self.geocoding_helper.get_insee_and_post_with_gps(2.3522, 48.8566)

        mock_get.assert_called_once_with(reverse_geocoding,
                                         params={"index": "address, poi", "lon": 2.3522, "lat": 48.8566, "limit": 1})
        assert insee is None
        assert postcode == 75001

    def test_missing_postcode(self, mocker, mock_missing_postcode_response):
        mock_get = mocker.patch("requests.get")
        mock_get.return_value.json.return_value = mock_missing_postcode_response
        mock_get.return_value.status_code = 200

        insee, postcode = self.geocoding_helper.get_insee_and_post_with_gps(2.3522, 48.8566)

        mock_get.assert_called_once_with(reverse_geocoding,
                                         params={"index": "address, poi", "lon": 2.3522, "lat": 48.8566, "limit": 1})
        assert insee == 75056
        assert postcode is None