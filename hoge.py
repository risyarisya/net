# coding:utf-8
import csv
keys = [u"住所", u"名前"]

def get_index_of_str_key(keys, lst):
  result = []
  for key in keys:
      result.append(lst.index(key))
  if len(result) != len(keys):
    raise ValueError

  return result

def read_csv(filename, keys, encoding): 
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    header = [ r.decode(encoding) for r in reader.next() ]
    result = []
    try:
      idx = get_index_of_str_key(keys, header)
    except:
      print("invalid csv format.")
      return [] 

    for row in reader:
      newdict = {}
      for k, i in zip(keys, idx):
        newdict[k] = row[i].decode(encoding)
      result.append(newdict)

  return result
 
result = read_csv('test.csv', keys, 'shift_jis')
print(result)
for r in result:
  print(r.get(keys[0]))
  print(r.get(keys[1]))
