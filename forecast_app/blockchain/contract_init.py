# forecast_app/blockchain/contract_init.py
import json
import os
import sys
import threading

import solcx
from django.conf import settings
from web3 import Web3

from forecast_app.blockchain.ganache_config import ganache_url


def init_contract():
    solcx.install_solc('v0.8.0')  # Specify the solc version here
    try:
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.default_account = web3.eth.accounts[0]  # Set the default account

        with open(os.path.join(settings.BLOCKCHAIN_DIR, "contract_abi.json"), "r") as abi_file:
            contract_abi = json.load(abi_file)

        contract_address = '0xE4A2a64582F1F15AF4a42C43Cbc90E435Ce66bb8'  # Use the correct deployed contract address
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        print("INFO [contract_init]: Contract initialized.")
        return contract, web3
    except Exception as e:
        print(f"ERROR [contract_init]: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_thread = threading.Thread(target=init_contract)
    init_thread.start()