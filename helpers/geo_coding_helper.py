import requests
from exceptions.GeoCodingExceptions import GeoCodingPointNotFound, GeoCodingMissingCityCodes
from helpers.external_adresses import reverse_geocoding, geo_search

class GeoCodingHelper:
    def get_insee_and_post_with_gps(self, longitude: float, latitude: float) -> tuple[int | None, int | None]:
        if not isinstance(longitude, float) or not isinstance(latitude, float):
            raise AttributeError("Longitude or Latitude is not a float.")

        return self._fetch_geojson_data(reverse_geocoding, params={"index": "address, poi", "lon": longitude, "lat": latitude, "limit": 1})

    def get_insee_and_post_with_address(self, address: str) -> tuple[int | None, int | None]:
        if not isinstance(address, str):
            raise AttributeError("Address is not a string.")

        return self._fetch_geojson_data(geo_search, params={"index": "address, poi", "q": address, "limit": 1})

    def _fetch_geojson_data(self, url: str, params: dict) -> tuple[int | None, int | None]:
        response: requests.Response = requests.get(url, params=params)
        response.raise_for_status()

        geojson_data = response.json()
        features = geojson_data.get("features", [])

        if not features:
            raise GeoCodingPointNotFound("No Geocoding Point found.")

        citycode = self._get_first_valid_code(features[0]["properties"].get("citycode"))
        postcode = self._get_first_valid_code(features[0]["properties"].get("postcode"))

        if citycode is None and postcode is None:
            raise GeoCodingMissingCityCodes("Both insee and postcode are missing.")

        return (int(citycode) if citycode is not None else None,
                int(postcode) if postcode is not None else None)

    def _get_first_valid_code(self, value: list[str] | str) -> str | None:
        if isinstance(value, list):
            for code in value:
                if isinstance(code, str) and len(code) == 5:
                    return code
            return None
        return value
