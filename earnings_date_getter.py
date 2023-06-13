import requests
from bs4 import BeautifulSoup
import csv

path = 'stock_codes.csv'
with open(path, encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        stock_code = row
        stock_code_str1 = str(stock_code)
        stock_code_str2 = stock_code_str1.replace('[', '')
        stock_code_str3 = stock_code_str2.replace("'", '')
        stock_code_str4 = stock_code_str3.replace(']', '')
        print(stock_code_str4)
        url = 'https://www.nikkei.com/markets/kigyo/money-schedule/kessan/ResultFlag=3&kwd=' + stock_code_str4
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        date_list = soup.select('th')
        print(date_list[8:])
        i = date_list[8:]
        n1 = str(i)
        n2 = n1.replace('[', '')
        n3 = n2.replace('<', '')
        n4 = n3.replace('t', '')
        n5 = n4.replace('h', '')
        n6 = n5.replace('>', '')
        n7 = n6.replace(']', '')
        with open('earnings_date.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([n7, stock_code_str4])
