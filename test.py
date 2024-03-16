import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def convert_to_ad(date_str):
    year, month, day = date_str.split('/')
    year = str(int(year) + 1911)  # Convert ROC year to AD year
    return f'{year}-{month}-{day}'

def fetch_stock_data(date, stock_no):
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    print(response.text[:500])
    if response.status_code == 200:
        # 分割响应文本为行，并过滤掉不需要的行
        lines = response.text.split('\n')
        # 确保数据行至少包含某些关键词，这里使用'成交股數'作为一个示例关键词
        valid_lines = [line for line in lines if '成交股數' in line or line.replace('"', '').replace(',', '').isdigit()]
        content = "\n".join(valid_lines)
        if content:
            try:
                df = pd.read_csv(StringIO(content), header=0)  # header=0 表示第一行是列名
                return df
            except pd.errors.EmptyDataError:
                print(f"No data to parse for {date_str} for stock {stock_no}.")
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
        df_all['日期'] = pd.to_datetime(df_all['日期'])
        # 转换收盘价为数值类型
        df_all['收盤價'] = pd.to_numeric(df_all['收盤價'].str.replace(',', ''), errors='coerce')
        
        plt.figure(figsize=(14, 7))
        plt.plot(df_all['日期'], df_all['收盤價'], marker='o', linestyle='-', color='b')
        plt.title(f'Stock No. {stock_no} Closing Price')
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
