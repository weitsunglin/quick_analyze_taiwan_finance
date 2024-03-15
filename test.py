import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

def fetch_stock_data(stock_code):
    url = f'https://www.cnyes.com/twstock/ps_historyprice.aspx?code={stock_code}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Attempt to more accurately select the correct elements
        # This assumes the structure of your table has specific identifiable patterns or tags around dates and prices
        # Adjust these selectors based on the actual HTML structure
        prices_elements = soup.select('td.rt:not(.percentage)')  # Example selector, adjust based on actual HTML
        dates_elements = soup.select('td.cr')  # Assuming 'cr' class is correct for dates
        
        # Ensure we're getting the expected elements
        if not prices_elements or not dates_elements:
            print("No data found")
            return None
        
        prices = []
        dates = []
        
        for price in prices_elements:
            try:
                cleaned_price = float(price.text.replace(',', '').replace('%', ''))
                prices.append(cleaned_price)
            except ValueError:
                continue  # Skip invalid prices
        
        for date in dates_elements:
            # Assuming date text is valid, but adjust validation as needed
            dates.append(date.text)
        
        # Trim lists to match the shortest one to avoid mismatch
        min_length = min(len(prices), len(dates))
        prices = prices[:min_length]
        dates = dates[:min_length]
        
        return {'dates': dates, 'prices': prices}
    else:
        print(f"Failed to fetch data for stock {stock_code}")
        return None

def plot_stock_data(data, stock_code):
    if data:
        dates = pd.to_datetime(data['dates'])
        close_prices = data['prices']
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

        plt.title(f"Stock {stock_code} Closing Prices Over Time")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"C:/Users/User/Desktop/project/quick_analyze_stock/{stock_code}_closing_prices.png")

    else:
        print(f"No data to plot for stock {stock_code}.")

def main(stock_code):
    print(f"\nFetching data for stock {stock_code}...")
    data = fetch_stock_data(stock_code)
    plot_stock_data(data, stock_code)

if __name__ == "__main__":
    stock_code = "2356"
    main(stock_code)
