import requests
from external_adresses import reverse_geocoding

def get_insee_with_gps(longitude: float, latitude: float) -> int|None:
    if not isinstance(longitude, float) or not isinstance(latitude, float):
        raise AttributeError("Longitude or Latitude is not a float.")

    response: requests.Response = requests.get(reverse_geocoding, params={"lon": longitude, "lat": latitude, "limit" : 1})
    response.raise_for_status()

    geojson_data = response.json()

    if "citycode" not in geojson_data["features"][0]["properties"]:
        return None

    insee_code = geojson_data["features"][0]["properties"]["citycode"]

    return insee_code if insee_code else None


if __name__ == "__main__":
    print(get_insee_with_gps(-0.66015, 43.814601))
