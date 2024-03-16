import matplotlib.pyplot as plt

# 繪製走勢圖
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['USD/NTD'], label='USD/NTD')
plt.plot(df.index, df['RMB/NTD'], label='RMB/NTD')
plt.title('Daily Foreign Exchange Rates')
plt.xlabel('Date')
plt.ylabel('Rate')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# 儲存圖表
plt.savefig('/mnt/data/exchange_rates_chart.png')

plt.show()
