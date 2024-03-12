import requests

def fetch_stock_data(stock, date):
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

def save_to_txt(data, filename):
    if data and data["stat"] == "OK":
        with open(filename, 'w', encoding='utf-8') as txtfile:
            txtfile.write(f"股票代號: {data['title'].split()[1]}\n")
            txtfile.write(f"資料日期: {data['date']}\n")
            txtfile.write(f"{data['title']}\n")
            txtfile.write('  / '.join(data["fields"]) + "\n")
            txtfile.write("\n")
            for row in data["data"]:
                row[0] = convert_date(row[0])
                txtfile.write('  / '.join(row) + "\n")
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

def main(stocks, date):
    for stock in stocks:
        print(f"\nFetching data for stock {stock}...")
        data = fetch_stock_data(stock, date)
        filename = f"stock_{stock}_{date}.txt"
        save_to_txt(data, filename)

if __name__ == "__main__":
    stocks = ["00929", "00919","2376","2357"]
    date = "202401"
    main(stocks, date)
