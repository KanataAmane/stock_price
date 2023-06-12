from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
from wasabi import msg
import os
import sys

text_file_path = './text'
if os.path.exists(text_file_path) == False:
	os.mkdir(text_file_path)

pdf_file_name=input('./pdf/ファイル名.pdf: ')

inputted_pdf_file_path = './pdf/'+pdf_file_name+'.pdf'

if os.path.exists(inputted_pdf_file_path) == False:
	msg.fail("Error: can't find such a file.")
	sys.exit()

generated_text_file_path = './text/'+pdf_file_name+'.txt'

if os.path.exists(generated_text_file_path) == True:
	msg.fail("Error: you have already such a file.")
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

with open(generated_text_file_path, 'w', encoding='utf-8') as f:
    f.write(text)
msg.good('Success!')