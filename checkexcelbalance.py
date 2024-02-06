import requests
import pandas as pd

def get_eth_balance(address, api_key):
    base_url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "tag": "latest",
        "apikey": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data.get("result", 0)) / 10**18
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}")
        return None

# Replace 'your_etherscan_api_key' with your actual API key
api_key = "J1Z5DPIB2NHUUEMJ9TP39DW76IBWCXTP37"

# Specify the correct path to the Excel file using double backslashes or a raw string
excel_file_path = r'C:\Users\perfr\Desktop\balance\balance.xlsx'

# Read the Excel file without a header
df = pd.read_excel(excel_file_path, header=None)

# Use list comprehension to retrieve Ethereum balances and add them to a new column
df['Balance'] = [get_eth_balance(address, api_key) for address in df.iloc[:, 0]]

# Save the updated DataFrame back to the same Excel file
with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
