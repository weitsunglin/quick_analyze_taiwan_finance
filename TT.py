import requests
import pandas as pd

# Central banks' data IDs mapped to their Chinese names
central_banks = {
    "FED": "美国联邦储备系统",  # Federal Reserve System
    "ECB": "欧洲中央银行",    # European Central Bank
    "BOJ": "日本银行",       # Bank of Japan
    "PBOC": "中国人民银行"   # People's Bank of China
}

base_url = "https://api.finmindtrade.com/api/v4/data"

# Function to fetch and display data for each central bank
def fetch_and_display_interest_rate_data(bank_id, bank_name):
    parameters = {
        "dataset": "InterestRate",
        "data_id": bank_id,
        "start_date": "1982-01-01",
    }
    response = requests.get(base_url, params=parameters)
    data = response.json()

    if 'data' in data and data['data']:
        df = pd.DataFrame(data['data'])
        df['full_country_name'] = bank_name  # Add full bank name for clarity
        print(f"Interest rate data for {bank_name} ({bank_id}):")
        print(df.head(), "\n")  # Print the first few rows of the DataFrame
    else:
        print(f"No data available for {bank_name} ({bank_id})\n")

# Iterate through each central bank and fetch interest rate data
for bank_id, bank_name in central_banks.items():
    fetch_and_display_interest_rate_data(bank_id, bank_name)
