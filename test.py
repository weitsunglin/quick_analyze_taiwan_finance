import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import StringIO

def fetch_stock_data(date, stock_no):
    """
    Fetch stock trading data for a given date and stock number.
    """
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    if response.status_code == 200:
        # Use StringIO to handle the CSV text, skip rows that don't start with a number (date)
        content = "\n".join([line for line in response.text.split('\n') if line.strip().startswith('"') or line.strip().isdigit()])
        if content:
            df = pd.read_csv(StringIO(content), header=1)
            return df
    return None

def main(stock_no, start_date, end_date):
    """
    Main function to fetch data, process it, and plot the closing prices.
    """
    current_date = start_date
    all_data = []

    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        print(f"Fetching data for {date_str}")
        data = fetch_stock_data(date_str, stock_no)
        if data is not None:
            all_data.append(data)
        current_date += timedelta(days=1)

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)

        # Preprocess and clean data
        df_all['日期'] = pd.to_datetime(df_all['日期'].str.replace('"', ''), format='%Y/%m/%d')
        df_all['收盤價'] = pd.to_numeric(df_all['收盤價'].str.replace(',', '').str.replace('"', ''), errors='coerce')

        # Plot closing prices
        plt.figure(figsize=(14, 7))
        plt.plot(df_all['日期'], df_all['收盤價'], marker='o', linestyle='-', color='b')
        plt.title(f'Stock No. {stock_no} Closing Price')
        plt.xlabel('Date')
        plt.ylabel('Closing Price (TWD)')
        plt.grid(True)
        plt.xticks(rotation=45)

        # Save plot to local file
        save_path = f"./{stock_no}_closing_prices.png"
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
        plt.close()
    else:
        print("No data fetched.")

if __name__ == "__main__":
    # Example: Fetch data for stock number 2330 from March 1, 2021, to March 31, 2021.
    stock_number = "2330"
    start = datetime(2021, 5, 1)
    end = datetime(2021, 5, 31)
    main(stock_number, start, end)
