# forecast_app/blockchain/contract_compile.py
import json
import os

import solcx
from django.conf import settings
from solcx import compile_standard


def compile_contract():
    solcx.install_solc('v0.8.0')  # Specify the solc version here

    with open(os.path.join(settings.BLOCKCHAIN_DIR, "bike_forecast.sol"), "r") as file:
        bike_forecast_source = file.read()

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {"bike_forecast.sol": {"content": bike_forecast_source}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version='0.8.0')  # Specify the solc version here

    with open(os.path.join(settings.BLOCKCHAIN_DIR, "contract_abi.json"), "w") as abi_file:
        json.dump(compiled_sol["contracts"]["bike_forecast.sol"]["BikeForecast"]["abi"], abi_file)

    print("INFO [contract_compile]: Contract compiled and ABI saved.")


if __name__ == "__main__":
    compile_contract()
