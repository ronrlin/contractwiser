#!/usr/bin/python
from pymongo import MongoClient

"""

"""
def clear_db():
   client = MongoClient('localhost', 27017)
   client['wiser_db'].drop_collection('classified')
   print("drop 'classified' collection...")
   client.drop_database('wiser_db')
   print("drop wiser_db...")
   client.close()

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
def create_db():
   client = MongoClient('localhost', 27017)
   print(client.database_names())
   db = client['wiser_db']
   print("created wiser_db...")
   collection = db['classified']
   print("created 'classified' collection...")
   import csv
   agreements = list()

   # this file is not stored in github
   with open('./archive/classify-temp.csv', 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      for row in spamreader:
         agree = {}
         agree['filename'] = row[0]
         agree['category'] = row[1] 
         agreements.append(agree)

   result = collection.insert_many(agreements)
   print("new records created")
   print(len(result.inserted_ids))
   client.close()

class WiserDatabase(object):
   def __init__(self):
      self.client = MongoClient('localhost', 27017)
      self.db = self.client['wiser_db']
      self.collection = self.db['classified']

   """
   Returns records (key/value pairs) corresponding to records with a certain value
   for the 'filename' value.

   Parameters

   filename : string

   returns Cursor
   """
   def fetch_by_filename(self, filename):
      result = self.collection.find_one({'filename' : filename})
      return result

   """
   Returns records (key/value pairs) corresponding to records with a certain value
   for the 'category' value.

   Parameters

   returns Cursor
   """
   def fetch_by_category(self, category):
      results = self.collection.find({'category' : category})
      return results

   """
   Returns a list of the 'category' names.  Categories are different names for 
   the agreements in the ContractWiser repository.

   returns a list
   """
   def get_category_names(self):
      return self.collection.distinct("category")

