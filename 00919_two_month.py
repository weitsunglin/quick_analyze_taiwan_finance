import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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
                    try:
                        year, month, day = map(int, date_str.split('/'))
                    except ValueError:
                        continue
                    gregorian_year = year + 1911
                    date = datetime(gregorian_year, month, day)
                    closing_price = float(parts[6])
                    dates.append(date)
                    prices.append(closing_price)
    return dates, prices

def get_previous_month(date):
    first_day_of_current_month = date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_previous_month.strftime("%Y%m%d")

def plot_stock_data(dates, prices, stock_no):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, marker='o', linestyle='-', color='b')
    plt.title(f'Stock No. {stock_no} Closing Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (TWD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"C:/Users/User/Desktop/project/quick_analyze_stock/{stock_no}_two_month_closing_prices.png")

if __name__ == "__main__":
    stock_number = "00919"
    current_date = datetime.now()
    current_month_str = current_date.strftime("%Y%m01")
    previous_month_str = get_previous_month(current_date)

    prev_dates, prev_prices = fetch_stock_data(previous_month_str, stock_number)
    curr_dates, curr_prices = fetch_stock_data(current_month_str, stock_number)

    all_dates = prev_dates + curr_dates
    all_prices = prev_prices + curr_prices

    plot_stock_data(all_dates, all_prices, stock_number)