import requests
from bs4 import BeautifulSoup
import csv

count=0
path = './stock_codes.csv'
with open(path, encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        stock_code = row
        stock_code_str = str(stock_code)
        stock_code_str = stock_code_str.replace('[', '')
        stock_code_str = stock_code_str.replace("'", '')
        stock_code_str = stock_code_str.replace(']', '')
        print(stock_code_str)
        url = 'https://www.nikkei.com/markets/kigyo/money-schedule/kessan/ResultFlag=3&kwd=' + stock_code_str
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        date_list = soup.select('th')
        print(date_list[8:])
        i = date_list[8:]
        n = str(i)
        n = n.replace('[', '')
        n = n.replace('<', '')
        n = n.replace('t', '')
        n = n.replace('h', '')
        n = n.replace('>', '')
        n = n.replace(']', '')
        count = count + 1
        print(count)
        with open('./earnings_date.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([n, stock_code_str])
