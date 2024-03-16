import requests
import pandas as pd

# Central banks' data IDs
data_ids = {
    "BOE": "英格蘭銀行",
    "RBA": "澳洲儲備銀行",
    "FED": "聯邦準備銀行",
    "PBOC": "中國人民銀行",
    "BOC": "中國銀行",
    "ECB": "歐洲中央銀行",
    "RBNZ": "紐西蘭儲備銀行",
    "RBI": "印度儲備銀行",
    "CBR": "俄羅斯中央銀行",
    "BCB": "馬來西亞商業銀行",  # Note: This might be a mistake. BCB typically refers to Brazil's Central Bank, Banco Central do Brasil.
    "BOJ": "日本銀行",
    "SNB": "瑞士國家銀行"
}

base_url = "https://api.finmindtrade.com/api/v4/data"
all_data = []

# Iterate through each central bank and fetch interest rate data
for data_id, bank_name in data_ids.items():
    parameter = {
        "dataset": "InterestRate",
        "data_id": data_id,
        "start_date": "1982-01-01",  # Adjust start date as needed
    }
    response = requests.get(base_url, params=parameter)
    data = response.json()
    
    # Check if data is fetched successfully
    if 'data' in data and data['data']:
        temp_df = pd.DataFrame(data['data'])
        temp_df['full_country_name'] = bank_name  # Add full bank name for clarity
        all_data.append(temp_df)
    else:
        print(f"No data available for {bank_name}")

# Combine all fetched data into a single DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# Display the combined data
print(combined_data.head())

# Optionally, you can save this data to a CSV file or perform further analysis
# combined_data.to_csv("central_banks_interest_rates.csv", index=False)
