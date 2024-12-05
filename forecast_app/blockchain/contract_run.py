# forecast_app/blockchain/contract_run.py
import solcx

from contract_compile import compile_contract
from contract_interaction import store_forecast, get_forecast
from contract_setup import deploy_contract
from contract_init import init_contract

def run_contract_operations():
    solcx.install_solc('v0.8.0')  # Specify the solc version here

    try:
        # Compile the contract
        compile_contract()
        print("INFO [contract_run]: Contract compiled successfully.")

        # Deploy the contract
        deploy_contract()
        print("INFO [contract_run]: Contract deployed successfully.")

        # Initialize the contract
        contract, web3 = init_contract()
        print("INFO [contract_run]: Contract initialized.")

        # Store forecast
        store_forecast(2, "New forecast data", contract, web3)
        print("INFO [contract_run]: Forecast stored successfully.")

        # Retrieve forecast
        result = get_forecast(2, contract, web3)
        if result:
            forecast_data, timestamp = result
            print(f"INFO [contract_run]: Retrieved forecast data: {forecast_data}, Timestamp: {timestamp}")
        else:
            print("ERROR [contract_run]: Failed to retrieve forecast data.")

    except Exception as e:
        print(f"ERROR [contract_run]: {str(e)}")

if __name__ == "__main__":
    run_contract_operations()