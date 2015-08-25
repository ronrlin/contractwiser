#!/usr/bin/python
from pymongo import MongoClient

"""
TODO: Create a unique index on 'filename'.
TODO: Check for exceptions in the case that uniqueness is broken.
TODO: Consider more robust exception handling.

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

def clear_db():
   """ Empty the database """
   client = MongoClient('localhost', 27017)
   client['wiser_db'].drop_collection('classified')
   print("drop 'classified' collection...")
   client.drop_database('wiser_db')
   print("drop wiser_db...")
   client.close()

def create_db():
   client = MongoClient('localhost', 27017)
   print(client.database_names())
   db = client['wiser_db']
   print("created wiser_db...")
   collection = db['classified']
   print("created 'classified' collection...")
   #collection.createIndex( { 'filename': "hashed" } )
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

def create_db_new():
   """ Creates the database for the new dataset """   
   client = MongoClient('localhost', 27017)
   print(client.database_names())
   db = client['wiser_db']
   print("created wiser_db...")
   collection = db['classified']
   print("created 'classified' collection...")
   #collection.createIndex( { 'filename': "hashed" } )
   import csv
   agreements = list()

   # this file is not stored in github
   with open('./classifier-new-data.csv', 'r') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
      for row in spamreader:
         agree = {}
         agree['filename'] = row[0].join(".txt")
         agree['category'] = row[1] 
         agreements.append(agree)

   result = collection.insert_many(agreements)
   print("new records created")
   print(len(result.inserted_ids))
   client.close()

class WiserDatabase(object):
   """ """
   def __init__(self):
      self.client = MongoClient('localhost', 27017)
      self.db = self.client['wiser_db']
      self.collection = self.db['classified']

   def fetch_by_filename(self, filename):
      """
      Returns records (key/value pairs) corresponding to records with a certain value
      for the 'filename' value.

      :param filename: string

      returns Cursor
      """
      result = self.collection.find_one({'filename' : filename})
      return result

   def fetch_by_category(self, category):
      """
      Returns records (key/value pairs) corresponding to records with a certain value
      for the 'category' value.

      :param category: matching a query on all records.

      returns Cursor
      """
      results = self.collection.find({'category' : category})
      return results

   def get_category_names(self):
      """
      Returns a list of the 'category' names.  Categories are different names for 
      the agreements in the ContractWiser repository.  Examples include 'CONVERTIBLE'
      for Convertible Note agreements, etc...

      returns a list
      """
      return self.collection.distinct("category")

   def add_record(self, filename, category):
      """ Add a record to the wiser_db """
      new_record = { 'filename' : filename, 'category' : category }
      result = self.collection.insert_one(new_record)
      print("one (1) new record created: " + result.inserted_id)
      return result.inserted_id
