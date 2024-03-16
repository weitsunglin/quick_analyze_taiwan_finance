import requests
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_stock_data(date, stock_no):
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    dates, prices = [], []
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            if line.count('",') > 8:
                parts = line.split('","')
                if len(parts) >= 7:
                    date_str = parts[0].replace('"', '')
                    # Attempt to split the date string and convert to integers
                    try:
                        year, month, day = map(int, date_str.split('/'))
                    except ValueError:
                        # Skip the header or any row that cannot be converted to integers
                        continue
                    # Convert ROC year to Gregorian year
                    gregorian_year = year + 1911
                    date = datetime(gregorian_year, month, day)
                    closing_price = float(parts[6])
                    dates.append(date)
                    prices.append(closing_price)
    return dates, prices

def plot_stock_data(dates, prices, stock_no):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, marker='o', linestyle='-', color='b')
    plt.title(f'Stock No. {stock_no} Closing Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (TWD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    stock_number = "2330"
    date = "20240301"
    dates, prices = fetch_stock_data(date, stock_number)
    plot_stock_data(dates, prices, stock_number)
