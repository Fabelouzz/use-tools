import requests
import json

def bitcoin_stats(input_str):
    """
    Fetch current Bitcoin statistics from the CoinGecko API.

    Parameters:
    input_str (str): A JSON string representing a dictionary with keys 'currency' and 'fields'.
                     Example: '{"currency": "usd", "fields": ["current_price", "market_cap", "total_volume"]}'

    Returns:
    str: The formatted result of the requested Bitcoin statistics.

    Raises:
    Exception: If an error occurs during the API request or data parsing.
    ValueError: If the input is invalid.
    """
    # Clean and parse the input string
    try:
        # Replace single quotes with double quotes
        input_str_clean = input_str.replace("'", "\"")
        # Remove any extraneous characters such as trailing quotes
        input_str_clean = input_str_clean.strip().strip("\"")

        input_dict = json.loads(input_str_clean)
        currency = input_dict['currency']
        fields = input_dict['fields']
    except (json.JSONDecodeError, KeyError) as e:
        return str(e), "Invalid input format. Please provide a valid JSON string."

    # Define the URL for the CoinGecko API request
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&ids=bitcoin"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return str(e), "Error during API request."

    if not data:
        return "No data received from the API."

    # Extract the requested fields from the API response
    bitcoin_data = data[0]
    result = {field: bitcoin_data.get(field, "Field not available") for field in fields}
    
    result_formatted = f"\n\nBitcoin Statistics:\n" + "\n".join([f"{key}: {value}" for key, value in result.items()]) + "\nFetched using bitcoin_stats."
    return result_formatted
