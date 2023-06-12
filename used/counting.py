# -*- coding: utf-8 -*-
from wasabi import msg

text = ''

if len(text) == 0:
	text_file_name = input('./text/ファイル名.txt: ')

f = open('./text/'+text_file_name+'.txt', 'r')
text = f.read()
f.close()

print('増 =>', text.count('増'))
positive = text.count('増')

print('上回 =>', text.count('上回'))
positive = positive + text.count('上回')

print('減 =>', text.count('減'))
negative = text.count('減')

print('下回 =>', text.count('下回'))
negative = negative + text.count('下回')

if positive != 0 or negative != 0:
	msg.good('Success!')
	print('ポジティブ率=>', positive/(positive+negative))
else:
	msg.fail('Error!')
