import csv
import datetime
import pandas_datareader as web

ticker_symbol = '2559'
ticker_symbol_dr = ticker_symbol + '.JP'
date = '2023-05-12'
date_format = '%Y-%m-%d'
dt = datetime.datetime.strptime(date, date_format)
start = dt

df_start = web.DataReader(ticker_symbol_dr, 'stooq', start=start, end=start)
print(df_start)

pre_day_price_df = df_start['Close'][0]
pre_day_price_int = pre_day_price_df.item()
print(f'前日の終値 => {pre_day_price_int}\n')

with open('./2559.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([pre_day_price_int, start])

for i in range(100):
    start = start + datetime.timedelta(days=7)

    df_start = web.DataReader(
        ticker_symbol_dr, 'stooq', start=start, end=start)
    print(df_start)

    pre_day_price_df = df_start['Close'][0]
    pre_day_price_int = pre_day_price_df.item()
    print(f'前日の終値 => {pre_day_price_int}\n')

    with open('./2559.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([pre_day_price_int, start])
