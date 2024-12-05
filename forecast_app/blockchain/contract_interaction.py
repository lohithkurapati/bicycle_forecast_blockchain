# forecast_app/blockchain/contract_interaction.py
import json
import pandas as pd

def convert_timestamps(obj):
    """
    Recursively converts pandas Timestamp objects in the given object to ISO 8601 strings.
    """
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()  # Convert Timestamp to ISO 8601 string
    elif isinstance(obj, list):
        return [convert_timestamps(item) for item in obj]  # Handle lists
    elif isinstance(obj, dict):
        return {key: convert_timestamps(value) for key, value in obj.items()}  # Handle dictionaries
    return obj  # Return the object unchanged if not a Timestamp

def store_forecast(id, forecast_data, contract, web3):
    try:
        # Convert all Timestamps in forecast_data to JSON-serializable format
        forecast_data = convert_timestamps(forecast_data)

        # Convert forecast_data to a JSON string
        forecast_data_json = json.dumps(forecast_data)

        # Ensure the ID is an integer (matches uint256 type in Solidity)
        id = int(id)

        # Get the from address (ensure it's in checksum format)
        from_address = web3.eth.default_account
        if not isinstance(from_address, str):
            from_address = web3.toChecksumAddress(from_address)

        # Call the contract function
        tx_hash = contract.functions.storeForecast(id, forecast_data_json).transact({'from': from_address})

        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"INFO [contract_interaction]: Forecast {id} stored with data {forecast_data_json}")
    except Exception as e:
        print(f"ERROR [contract_interaction]: Failed to store forecast - {str(e)}")


def get_forecast(id, contract, web3):
    try:
        forecast_data, timestamp = contract.functions.getForecast(id).call()
        print(f"INFO [contract_interaction]: Retrieved Forecast ID: {id} with data: {forecast_data}")
        return forecast_data, timestamp
    except Exception as e:
        print(f"ERROR [contract_interaction]: Failed to retrieve forecast - {str(e)}")
        return None