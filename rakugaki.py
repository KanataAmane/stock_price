import sys
import re

text = open('./text/JPX_full.txt', 'r')
i = 0
for l in text:
	i = i+1
	print(f'{i}\n{l}')
	result_of_date = re.findall(('.+年12345月.+日\n'), l)
	check = []
	if not result_of_date == check:
		print(result_of_date)
		break
if result_of_date == check:
	print(f'{result_of_date}, <=')