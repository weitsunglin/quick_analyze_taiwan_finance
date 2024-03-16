import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def convert_to_ad(date_str):
    try:
        year, month, day = date_str.split('/')
        year = str(int(year) + 1911)  # 将民国纪年转换为公元纪年
        return f'{year}-{month}-{day}'
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return date_str

def fetch_stock_data(date, stock_no):
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split('\n')
        # 过滤出有效的数据行
        valid_lines = [line for line in lines if "110/" in line]
        content = "\n".join(valid_lines)
        if content:
            try:
                df = pd.read_csv(StringIO(content), header=None)
                df = df.iloc[:, [0, 6]]  # 选取日期和收盘价列
                df.columns = ['日期', '收盤價']  # 重新命名列
                return df
            except pd.errors.EmptyDataError as e:
                print(f"No data to parse for {date} for stock {stock_no}. Error: {e}")
    else:
        print(f"Failed to retrieve data for stock number {stock_no} on {date}, status code: {response.status_code}")
    return None

def main(stock_no, start_date, end_date):
    all_data = []
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        data = fetch_stock_data(date_str, stock_no)
        if data is not None and not data.empty:
            all_data.append(data)
        current_date += timedelta(days=1)

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        # 处理日期格式
        df_all['日期'] = df_all['日期'].apply(convert_to_ad)
        df_all['日期'] = pd.to_datetime(df_all['日期'], errors='coerce')

        # 检查'收盤價'是否为字符串，如果是，则替换逗号
        if df_all['收盤價'].dtype == object:
            df_all['收盤價'] = df_all['收盤價'].str.replace(',', '')
        df_all['收盤價'] = pd.to_numeric(df_all['收盤價'], errors='coerce')

        plt.figure(figsize=(14, 7))
        plt.plot(df_all['日期'], df_all['收盤價'], marker='o', linestyle='-', color='b')
        plt.title(f'Stock No. {stock_no} Closing Price Trend')
        plt.xlabel('Date')
        plt.ylabel('Closing Price (TWD)')
        plt.xticks(rotation=45)
        plt.grid(True)

        save_path = f"{stock_no}_closing_prices.png"
        plt.savefig(save_path)
        plt.show()
        print(f"Plot saved to {save_path}")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    stock_number = "2330"
    start = datetime(2021, 5, 1)
    end = datetime(2021, 5, 31)
    main(stock_number, start, end)
