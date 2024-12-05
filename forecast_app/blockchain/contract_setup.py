# forecast_app/blockchain/contract_setup.py
import json
import os

import solcx
from django.conf import settings
from solcx import compile_source
from web3 import Web3


def deploy_contract():

    solcx.install_solc('v0.8.0')  # Specify the solc version here

    with open(os.path.join(settings.BLOCKCHAIN_DIR, "bike_forecast.sol"), "r") as file:
        bike_forecast_source = file.read()

    compiled_sol = compile_source(bike_forecast_source, solc_version='0.8.0')  # Specify the solc version here
    contract_interface = compiled_sol["<stdin>:BikeForecast"]

    web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Update to your Ganache URL
    web3.eth.default_account = web3.eth.accounts[0]

    BikeForecast = web3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
    tx_hash = BikeForecast.constructor().transact({'from': web3.eth.default_account})  # Specify the from address
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print(f"INFO [contract_setup]: Contract deployed at {contract_address}")
    with open("contract_abi.json", "w") as abi_file:
        json.dump(contract_interface["abi"], abi_file)

    print(f"INFO [contract_setup]: Contract deployed at {contract_address}")

if __name__ == "__main__":
    deploy_contract()