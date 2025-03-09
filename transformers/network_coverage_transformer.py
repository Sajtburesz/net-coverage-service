from models.coverage import NetworkCoverage
from helpers.lambert93_to_gps import lambert93_to_gps
from helpers.get_insee_and_post_with_gps import get_insee_and_post_with_gps

def transform_network_coverage(model_instance: NetworkCoverage, record: dict[str, str]) -> None:
    model_instance.operator = int(record["Operateur"])
    model_instance.type_2g = bool(int(record["2G"]))
    model_instance.type_3g = bool(int(record["3G"]))
    model_instance.type_4g = bool(int(record["4G"]))

    long, lat = lambert93_to_gps(record["x"], record['y'])

    try:
        insee_code, post_code = get_insee_and_post_with_gps(long, lat)
    except:
        raise KeyError

    model_instance.insee_code = insee_code
    model_instance.post_code = post_code
