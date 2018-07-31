#coding:utf-8                                                                                                       
import glob
import xlrd
import os
from datetime import datetime, timedelta

def excel_date(num):
  return (datetime(1899, 12, 30) + timedelta(days=num)).strftime('%Y/%m/%d')

def makeReview(filename, sheet):
  sheet = book.sheet_by_index(1)
  for r in range(2, sheet.nrows):
    # B3                                                                                                            
    revision = sheet.cell_value(rowx=r, colx=1)
    comment = sheet.cell_value(rowx=r, colx=2).replace('\n', ' ')
    datestr = excel_date(sheet.cell_value(rowx=r, colx=3))
    name = sheet.cell_value(rowx=r, colx=4)
    str = "{} : {} \t {} \t {} \t {}".format(os.path.basename(filename), revision, datestr, name, comment)
    print(str)

def checkTitle(filename, book):
  sheet = book.sheet_by_index(0)

  # C9                                                                                                              
  title = sheet.cell_value(rowx=8, colx=2)
  str = "{} \t {}".format(os.path.basename(filename), title)
  print(str)

file_lst = glob.glob('./test/*.xls')
for filename in file_lst:
  book = xlrd.open_workbook(filename)
  checkTitle(filename, book)
#  makeReview(filename, book)    
