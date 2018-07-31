#coding:utf-8
import glob
import xlrd
import os
from datetime import datetime, timedelta

def excel_date(num):
  return (datetime(1899, 12, 30) + timedelta(days=num)).strftime('%Y/%m/%d')  

file_lst = glob.glob('./test/*.xls')
for filename in file_lst:
  book = xlrd.open_workbook(filename)
  sheet = book.sheet_by_index(0)

  for r in range(2, sheet.nrows):
    revision = sheet.cell_value(rowx=r, colx=1)
    comment = sheet.cell_value(rowx=r, colx=2).replace('\n', ' ')
    datestr = excel_date(sheet.cell_value(rowx=r, colx=3))
    name = sheet.cell_value(rowx=r, colx=4)
    str = "{} : {} \t {} \t {} \t {}".format(os.path.basename(filename), revision, datestr, name, comment)
    print(str)

