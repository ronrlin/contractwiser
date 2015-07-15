#!/usr/bin/python
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
print(client.database_names())
db = client['wiser_db']
collection = db['classified']

import csv
agreements = list()
agree = dict()

# this file is not stored in github
with open('./archive/classify-temp.csv', 'r') as csvfile:
   spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
   for row in spamreader:
      agree['filename'] = row[0]
      agree['category'] = row[1] 
      agreements.append(agree)

"""
agreements = [
   {
      'filename' : '891daf5deebf3e31b7bb1c2970ac1c507d50818aa4db2dfd0b7e9b344a340202',
      'category' : 'convertible',  
   }, 
   {
      'filename' : '20d22f00ed2f67c68ff0d81975242187eb07a0c7499da0e16e83f11b4c0372a4',
      'category' : 'indenture',        
   }]
"""

result = collection.insert_many(agreements)
print(result.inserted_ids)

print('new database created')
print(client.database_names())
print('new collection created')
print(client.wiser_db.collection_names())

client.close()

#from pymongo import Connection
# client.drop_database('wiser_db')
# client['wiser_db'].drop_collection('classified')
