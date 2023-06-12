import sys
import re

text = open('./text/日本取引所_full.txt', 'r')
i = 0
for line in text:
    i = i+1
    print(f'{i}\n{line}')
    result_of_date = re.findall(('.+年.+月.+日\n'), l)
    check = []
    if not result_of_date == check:
        print(f'{result_of_date},<=提出日')
        break
if result_of_date == check:
    print(f'{result_of_date},<=提出日')
    print(line)
