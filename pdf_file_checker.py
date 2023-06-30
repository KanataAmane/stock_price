import os
import csv
import sys

rows = []
i = 1
with open('./current_codes_list.csv', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)
    number_of_rows = len(rows)
    for i in range(number_of_rows):
        file_name = str(rows[i])
        file_name = file_name.replace('[', '')
        file_name = file_name.replace(']', '')
        file_name = file_name.replace("'", '')

        pdf_file_path = './pdf2/'+file_name+'.pdf'
        if os.path.exists(pdf_file_path) is True:
            os.remove(pdf_file_path)
        i = i + 1

        if i == 168:
            sys.exit()
