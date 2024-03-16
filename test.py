import requests

def fetch_print_stock_data(date, stock_no):
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split('\n')  # Split the text into lines
        for line in lines:
            if line.count('",') > 8:  # Ensure the line has enough columns
                parts = line.split('","')  # Split the line into columns
                if len(parts) >= 7:  # Ensure there are enough parts
                    date = parts[0].replace('"', '')  # Remove extra quotes from the date
                    closing_price = parts[6]  # Get the closing price
                    print(f"Date: {date}, Closing Price: {closing_price}")

if __name__ == "__main__":
    stock_number = "2330"
    date = "20240301"
    fetch_print_stock_data(date, stock_number)
