import os
import sys
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
from wasabi import msg

text_file_path = './text'
if os.path.exists(text_file_path) == False:
	os.mkdir(text_file_path)

pdf_file_name=input('./pdf/ファイル名.pdf: ')

inputted_pdf_file_path = './pdf/'+pdf_file_name+'.pdf'

if os.path.exists(inputted_pdf_file_path) == False:
	msg.fail("Error: can't find the file.")
	sys.exit()


fp = open(inputted_pdf_file_path, 'rb')

outfp = StringIO()

rmgr = PDFResourceManager()
lprms = LAParams()
device = TextConverter(rmgr, outfp, laparams=lprms)
iprtr = PDFPageInterpreter(rmgr, device) 

for page in PDFPage.get_pages(fp):
    iprtr.process_page(page)
text = outfp.getvalue()
outfp.close()
device.close()
fp.close()
text = text.replace('\n', '')
text = text.replace(' ', '')
text = text.replace('　', '')
extracted_text = text.replace('', '')


index_start = extracted_text.find('【経営者による財政状態、経営成績及びキャッシュ・フローの状況の分析】')
#print(index_start)

index_end = extracted_text.find('【経営上の重要な契約等】')
#print(index_end)

clipped_text = extracted_text[index_start:index_end+12]
#print(clipped_text)

generated_text_file_path = './text/'+pdf_file_name+'.txt'

with open(generated_text_file_path, 'w') as f:
    f.write(clipped_text)


print('増 =>', clipped_text.count('増'))
positive = clipped_text.count('増')

print('上回 =>', clipped_text.count('上回'))
positive = positive + clipped_text.count('上回')

print('減 =>', clipped_text.count('減'))
negative = clipped_text.count('減')

print('下回 =>', clipped_text.count('下回'))
negative = negative + clipped_text.count('下回')

if positive != 0 or negative != 0:
	msg.good('Success!')
	positive_ratio = positive/(positive+negative)
	print('ポジティブ率=>', positive_ratio)
else:
	msg.fail('Error!: both positive and negative are null.')

with open('stock_list.csv') as f:
	lines=f.readlines()

lines_strip = [line.strip() for line in lines]
code_and_names = [line_s for line_s in lines_strip if pdf_file_name in line_s ]
list_empty = []
if not code_and_names == list_empty:
	print(code_and_names)
else:
	msg.warn("Warning!: couldn't find the stock in 'list_of_stocks.csv'")