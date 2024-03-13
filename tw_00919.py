import requests
import matplotlib.pyplot as plt
import pandas as pd


def fetch_stock_data(stock, date):
    # 上市api url，興櫃沒有哦
    address = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock}"
    response = requests.get(address)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for stock {stock}")
        return None

def convert_date(data_ROC):
    date_arr = data_ROC.split("/")
    new_year = int(date_arr[0]) + 1911
    return f"{new_year}-{date_arr[1].zfill(2)}-{date_arr[2].zfill(2)}"

def plot_stock_data(data, stock):
    if data and data["stat"] == "OK":
        dates = [convert_date(row[0]) for row in data["data"]]
        close_prices = [float(row[6].replace(',', '')) for row in data["data"]]
        plt.figure(figsize=(14, 7))

        plt.plot(dates, close_prices, marker='o', linestyle='-', color='grey', label='Closing Price')

        previous_price = None
        for i, price in enumerate(close_prices):
            if previous_price is None:
                color = 'black'
            elif price > previous_price:
                color = 'red'
            elif price < previous_price:
                color = 'green'
            else:
                color = 'black'

            plt.plot(dates[i], price, marker='o', color=color)
            plt.text(dates[i], price, f'{price}', color=color, fontsize=8, verticalalignment='bottom', horizontalalignment='center')
            previous_price = price

        plt.title(f"Stock {stock} Closing Prices Over Time")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()        
        plt.savefig(f"C:/Users/User/Desktop/project/quick_analyze_stock/{stock}_closing_prices.png")

    else:
        print(f"No data to plot for stock {stock}.")



def main(stocks, date):
    for stock in stocks:
        print(f"\nFetching data for stock {stock}...")
        data = fetch_stock_data(stock, date)
        plot_stock_data(data, stock)

if __name__ == "__main__":
    stocks = [ "00919"]
    date = "202401"
    main(stocks, date)
