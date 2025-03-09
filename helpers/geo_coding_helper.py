import requests
from external_adresses import reverse_geocoding, geo_search

class GeoCodingHelper:
    def get_insee_and_post_with_gps(self, longitude: float, latitude: float) -> (int, int):
        if not isinstance(longitude, float) or not isinstance(latitude, float):
            raise AttributeError("Longitude or Latitude is not a float.")
        response: requests.Response = requests.get(reverse_geocoding, params={"index": "address, poi", "lon": longitude, "lat": latitude, "limit" : 1})
        response.raise_for_status()

        geojson_data = response.json()

        return int(self._get_first_valid_code(geojson_data["features"][0]["properties"]["citycode"])), int(self._get_first_valid_code(geojson_data["features"][0]["properties"]["postcode"]))

    def get_insee_and_post_with_address(self, address: str) -> (int, int):
        if not isinstance(address, str):
            raise AttributeError("Address is not a string.")

        response: requests.Response = requests.get(geo_search, params={"index": "address, poi", "q": address, "limit": 1})
        response.raise_for_status()

        geojson_data = response.json()
        return int(self._get_first_valid_code(geojson_data["features"][0]["properties"]["citycode"])), int(self._get_first_valid_code(geojson_data["features"][0]["properties"]["postcode"]))


    def _get_first_valid_code(self, value: list[str]| str) -> str|None:
        if isinstance(value, list):
            for code in value:
                if isinstance(code, str) and len(code) == 5:
                    return code
            return None
        return value