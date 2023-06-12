#このファイルの保存先と同じディレクトリ内に"pdf"と"text"という名前のフォルダを作ること。

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO

pdf_file_name=input("変換したいファイル名: ")
print(pdf_file_name+".pdfをテキストファイルへ変換")
fp = open("./pdf/"+pdf_file_name+".pdf", 'rb')

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

text_file = "text/"+pdf_file_name+".txt"

with open(text_file, "w", encoding="utf-8") as f:
    f.write(text)