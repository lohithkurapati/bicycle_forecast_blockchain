# forecast_app/blockchain/test_contract.py
import json
import os

from django.conf import settings
from web3 import Web3

def test_contract():
    try:
        # Connect to Ganache
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.default_account = web3.eth.accounts[0]

        # Load contract ABI
        with open(os.path.join(settings.BLOCKCHAIN_DIR, "contract_abi.json"), "r") as abi_file:
            contract_abi = json.load(abi_file)

        # Contract address (replace with your deployed contract address)
        contract_address = '0x0C33bd7e668594e5f1fB3850cC60FEA2A054e2Bd'
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # Test storeForecast function
        tx_hash = contract.functions.storeForecast(1, "Test forecast data").transact({'from': web3.eth.default_account})
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Forecast stored: {receipt}")

        # Test getForecast function
        forecast_data, timestamp = contract.functions.getForecast(1).call()
        print(f"Retrieved forecast: {forecast_data}, Timestamp: {timestamp}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_contract()