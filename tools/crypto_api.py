import requests
import json

def crypto_stats(input_str):
    """
    Fetch current cryptocurrency statistics from the CoinGecko API for a specified cryptocurrency ID.

    Parameters:
    input_str (str): A JSON string representing a dictionary with keys 'crypto_id' and 'fields'.
                     Example: '{"crypto_id": "bitcoin", "fields": ["current_price", "market_cap", "total_volume"]}'

    Returns:
    str: The formatted result of the requested cryptocurrency statistics.

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
        crypto_id = input_dict['crypto_id']
        fields = input_dict['fields']
    except (json.JSONDecodeError, KeyError) as e:
        return str(e), "Invalid input format. Please provide a valid JSON string."

    # Define the URL for the CoinGecko API request
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={crypto_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return str(e), "Error during API request."

    if not data:
        return "No data received from the API."

    # Extract the requested fields from the API response
    crypto_data = data[0]
    result = {field: crypto_data.get(field, "Field not available") for field in fields}
    
    result_formatted = f"\n\n{crypto_id.capitalize()} Statistics:\n" + "\n".join([f"{key}: {value}" for key, value in result.items()]) + "\nFetched using crypto_stats."
    return result_formatted

