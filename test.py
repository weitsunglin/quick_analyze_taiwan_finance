import requests

def fetch_print_stock_data(date, stock_no):
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)

if __name__ == "__main__":
    stock_number = "2330"
    date = "20240301"
    fetch_print_stock_data(date, stock_number)
