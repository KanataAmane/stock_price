import os
import sys
import csv
import datetime
import unicodedata
import re
import pandas_datareader.data as web
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO
from wasabi import msg

counter = 0
SIGNAL = 'システムを終了します。'
rows = []
with open('./topix_codes_list.csv', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)
    number_of_rows = len(rows)
    for i in range(number_of_rows):
        file_name = str(rows[i])
        file_name = file_name.replace('[', '')
        file_name = file_name.replace(']', '')
        file_name = file_name.replace("'", '')
        print(file_name)

        # "text"フォルダの作成
        text_directory_path = './text'
        if os.path.exists(text_directory_path) is False:
            os.mkdir(text_directory_path)

        pdf_file_path = './pdf/'+file_name+'.pdf'
        if os.path.exists(pdf_file_path) is False:
            msg.fail("Error: can't find below file.", pdf_file_path)
            print(SIGNAL)
            sys.exit()

        # テキスト変換。
        fp = open(pdf_file_path, 'rb')

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

        # 全テキストを保存。
        full_text_file_path = './text/'+file_name+'_full.txt'
        with open(full_text_file_path, 'w') as f:
            f.write(text)

        # テキストの抜粋と保存。
        text_extracted = text.replace('\n', '')
        text_extracted = text_extracted.replace(' ', '')
        text_extracted = text_extracted.replace('　', '')
        extracted_text = text_extracted.replace('', '')

        index_start = extracted_text.find(
            '【経営者による財政状態、経営成績及びキャッシュ・フローの状況の分析】')
        if index_start == -1:
            msg.fail("Error!: can't find '【経営者による財政状態、"
                     "経営成績及びキャッシュ・フローの状況の分析】'.")
            print(pdf_file_path)
            sys.exit()

        index_end = extracted_text.find('【経営上の重要な契約等】')
        if index_end == -1:
            msg.fail("Error!: can't find '【経営上の重要な契約等】'.")
            print(pdf_file_path)
            sys.exit()

        text_extracted = extracted_text[index_start:index_end+12]

        text_file_path = './text/'+file_name+'_extracted.txt'
        with open(text_file_path, 'w') as f:
            f.write(text_extracted)

        # ポジティブ比の分析。
        print('増 =>', text_extracted.count('増'))
        positive = text_extracted.count('増')

        print('上回 =>', text_extracted.count('上回'))
        positive = positive + text_extracted.count('上回')

        print('減 =>', text_extracted.count('減'))
        negative = text_extracted.count('減')

        print('下回 =>', text_extracted.count('下回'))
        negative = negative + text_extracted.count('下回')

        if positive != 0 or negative != 0:
            msg.good('Success!')
            positive_ratio = positive/(positive+negative)
            print('ポジティブ率=>', positive_ratio)
        else:
            msg.fail('Error!: both positive and negative are null.')

        # 企業名や銘柄コードを表示。
        with open('./stock_list.csv') as f:
            lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        code_and_names = [
            line for line in lines_strip if file_name in line]
        list_empty = []
        if not code_and_names == list_empty:
            code_and_names = str(code_and_names)
            code_and_names = code_and_names.replace("'", '')
            print(code_and_names)
        else:
            msg.warn("Warning!: can't find the stock in 'list_of_stocks.csv'")
            code_and_names = ['該当なし']
            print(code_and_names)

        # 提出日の取得。
        with open(full_text_file_path) as f:
            full_text_list = f.readlines()

        for n in full_text_list:
            result_of_date = re.findall(('.+年.+月.+日\n'), n)
            check = []
            if not result_of_date == check:
                break

        if result_of_date == check:
            msg.warn("Warning!: can't find '提出日'")

        result_of_date = ''.join(result_of_date)
        result_of_date = result_of_date.replace('[]', '')
        result_of_date = result_of_date.replace('\n', '')

        normalized_result_of_date = unicodedata.normalize(
            'NFKC', result_of_date)

        result_of_date_format = '%Y年%m月%d日'
        dt = datetime.datetime.strptime(
            normalized_result_of_date, result_of_date_format)
        result_day = dt.date()

        print(f'提出日 => {result_day}')

        # 決算日の取得。
        with open('earnings_date.csv', encoding='utf-8-sig') as f:
            lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        earnings_date_list = [
            line_s for line_s in lines_strip if file_name in line_s]
        list_empty == []
        if earnings_date_list == list_empty:
            msg.error(
                "Error!: can't find the earnings date in 'earings_date.csv'")
            print(pdf_file_path)
            sys.exit()

        earnings_date_str = str(earnings_date_list[0])
        earnings_date_str = earnings_date_str.replace('[', '')
        earnings_date_str = earnings_date_str.replace("'", '')
        earnings_date_str = earnings_date_str.replace(']', '')
        earnings_date_str = earnings_date_str.replace(file_name, '')
        earnings_date_str = earnings_date_str.replace(',', '')

        earnings_date_format = '%Y/%m/%d/'
        dt = datetime.datetime.strptime(
            earnings_date_str, earnings_date_format)

        earnings_date = dt.date()
        print(f'決算日 => {earnings_date}')

        # 曜日の判定。
        start = earnings_date + datetime.timedelta(days=-1)
        end = earnings_date + datetime.timedelta(days=1)

        holiday = datetime.date(2023, 5, 8)
        if earnings_date == holiday:
            start = datetime.date(2023, 5, 8)

        start_day = start.weekday()
        if start_day == 6:
            start = earnings_date + datetime.timedelta(days=-3)

        if start_day == 5:
            earnings_date + datetime.timedelta(days=-2)

        holiday = datetime.date(2023, 5, 2)
        if earnings_date == holiday:
            end = datetime.date(2023, 5, 8)

        end_day = end.weekday()
        if end_day == 5:
            end = earnings_date + datetime.timedelta(days=3)

        if end_day == 6:
            end = earnings_date + datetime.timedelta(days=2)

        # 終値の取得。
        ticker_symbol = file_name
        ticker_symbol_dr = ticker_symbol + '.JP'

        df_start = web.DataReader(
            ticker_symbol_dr, 'stooq', start=start, end=start)

        pre_day_price_df = df_start['Close'][0]
        pre_day_price_int = pre_day_price_df.item()
        print(f'前日の終値 => {pre_day_price_int}')

        df_end = web.DataReader(ticker_symbol_dr, 'stooq', start=end, end=end)

        next_day_price_df = df_end['Close'][0]
        next_day_price_int = next_day_price_df.item()
        print(f'後日の終値 => {next_day_price_int}')

        # 同日のTOPIXの終値の取得。
        ticker_symbol_dr = '^TPX'

        df_start = web.DataReader(
            ticker_symbol_dr, 'stooq', start=start, end=start)

        pre_day_topix_price_df = df_start['Close'][0]
        pre_day_topix_price_int = pre_day_topix_price_df.item()
        print(f'TOPIXの前日の終値 => {pre_day_topix_price_int}')

        df_end = web.DataReader(ticker_symbol_dr, 'stooq', start=end, end=end)

        next_day_topix_price_df = df_end['Close'][0]
        next_day_topix_price_int = next_day_topix_price_df.item()
        print(f'TOPIXの後日の終値 => {next_day_topix_price_int}')

        # CSVに結果を出力。
        change_ratio = next_day_price_int/pre_day_price_int
        topix_change_ratio = next_day_topix_price_int/pre_day_topix_price_int
        with open('./results.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([file_name, positive_ratio,
                             pre_day_price_int, next_day_price_int,
                             change_ratio, code_and_names,
                             topix_change_ratio, earnings_date])

        msg.good(f'Success!: 銘柄コード=>{file_name}')
        counter = counter + 1
		print(f'カウンター=>{counter}')
