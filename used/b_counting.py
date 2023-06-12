# -*- coding: utf-8 -*-
from wasabi import msg

text = ''

if len(text) == 0:
	text = input('分析したいテキストを入力: ')

print('増加 =>', text.count('増加'))
positive = text.count('増加')

print('増収 =>', text.count('増収'))
positive = positive + text.count('増収')

print('増益 =>', text.count('増益'))
positive = positive + text.count('増益')

print('上回 =>', text.count('上回'))
positive = positive + text.count('上回')

print('減少 =>', text.count('減少'))
negative = text.count('減少')

print('減収 =>', text.count('減収'))
negative = negative + text.count('減収')

print('減益 =>', text.count('減益'))
negative = negative + text.count('減益')

print('下回 =>', text.count('下回'))
negative = negative + text.count('下回')

if positive != 0 or negative != 0:
	print('ポジティブ率=>', positive/(positive+negative))
else:
	msg.fail('Error!')