import pytest
from helpers.geo_coding_helper import GeoCodingHelper
from controllers.coverage_controller import CoverageController
from models import NetworkCoverage, NetworkProviders

class TestCoverageController:
    def test_coverage_check_with_gps(self, mocker, any_gps_param):
        self.geo_coding_helper = mocker.Mock(spec=GeoCodingHelper)
        self.geo_coding_helper.get_insee_and_post_with_gps.return_value = (12345, 67890)
        self.db_session = mocker.Mock()
        self.controller = CoverageController(self.geo_coding_helper, self.db_session)

        provider_a = NetworkProviders(operator=1, operator_name="OperatorA")
        provider_b = NetworkProviders(operator=2, operator_name="OperatorB")
        coverage_a = NetworkCoverage(
            insee_code=12345, post_code=67890, provider=provider_a,
            type_2g=True, type_3g=False, type_4g=True
        )
        coverage_b = NetworkCoverage(
            insee_code=12345, post_code=67890, provider=provider_b,
            type_2g=False, type_3g=True, type_4g=False
        )
        self.db_session.session.execute.return_value.scalars.return_value.all.return_value = [coverage_a, coverage_b]

        result = self.controller.coverage_check(any_gps_param)

        self.geo_coding_helper.get_insee_and_post_with_gps.assert_called_once_with(any_gps_param["lon"], any_gps_param["lat"])
        expected_result = {
            "OperatorA": {"2G": True, "3G": False, "4G": True},
            "OperatorB": {"2G": False, "3G": True, "4G": False}
        }
        assert result == expected_result

    def test_coverage_check_with_address(self, mocker, any_address_param):
        self.geo_coding_helper = mocker.Mock(spec=GeoCodingHelper)
        self.geo_coding_helper.get_insee_and_post_with_address.return_value = (12345, 67890)
        self.db_session = mocker.Mock()
        self.controller = CoverageController(self.geo_coding_helper, self.db_session)

        provider_a = NetworkProviders(operator=1, operator_name="OperatorA")
        coverage_a = NetworkCoverage(
            insee_code=12345, post_code=67890, provider=provider_a,
            type_2g=True, type_3g=True, type_4g=True
        )
        self.db_session.session.execute.return_value.scalars.return_value.all.return_value = [coverage_a]

        result = self.controller.coverage_check(any_address_param)

        self.geo_coding_helper.get_insee_and_post_with_address.assert_called_once_with(any_address_param["q"])
        expected_result = {
            "OperatorA": {"2G": True, "3G": True, "4G": True}
        }
        assert result == expected_result

    def test_coverage_check_invalid_gps(self, mocker, invalid_gps_param):
        self.geo_coding_helper = mocker.Mock(spec=GeoCodingHelper)
        self.db_session = mocker.Mock()
        self.controller = CoverageController(self.geo_coding_helper, self.db_session)

        with pytest.raises(ValueError, match="Longitude and Latitude must be valid numbers."):
            self.controller.coverage_check(invalid_gps_param)
