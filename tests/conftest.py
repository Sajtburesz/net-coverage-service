import pytest

@pytest.fixture
def mock_geocoding_response_no_list():
    """Fixture for a successful geocoding API response"""
    return {
        "features": [{
            "properties": {
                "citycode": "75056",
                "postcode": "75001"
            }
        }]
    }

@pytest.fixture
def mock_geocoding_response_with_list():
    return {
        "features": [{
            "properties": {
                "citycode": "75056",
                "postcode": ["75001", "8911123"]
            }
        }]
    }
@pytest.fixture
def mock_empty_response():
    """Fixture for an API response with no features"""
    return {"features": []}

@pytest.fixture
def mock_missing_codes_response():
    """Fixture for an API response missing citycode and postcode"""
    return {"features": [{"properties": {}}]}

@pytest.fixture
def mock_missing_citycode_response():
    """Fixture where only postcode is available, but citycode is missing"""
    return {
        "features": [{
            "properties": {
                "postcode": "75001"
            }
        }]
    }

@pytest.fixture
def mock_missing_postcode_response():
    """Fixture where only citycode is available, but postcode is missing"""
    return {
        "features": [{
            "properties": {
                "citycode": "75056"
            }
        }]
    }

@pytest.fixture
def invalid_gps_param():
    return {"lon": "invalid", "lat": "48.8566"}

@pytest.fixture
def any_address_param():
    return {"q": "Rue de Budapest Paris"}

@pytest.fixture
def any_gps_param():
    return {"lon": "2.3522", "lat": "48.8566"}
