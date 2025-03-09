from models.network_providers import NetworkProviders

def transform_network_providers(model_instance: NetworkProviders, record: dict[str, str]) -> None:
    model_instance.operator = int(record["MCCMNC"])
    model_instance.operator_name = str(record["Name"])
