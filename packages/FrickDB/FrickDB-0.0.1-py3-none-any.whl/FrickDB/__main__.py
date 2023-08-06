from .db import *
from .exceptions import *
import json
import os

class Client:
	client = HandlerDir()

	def insert_col(self, col):
		""" """
		return Col(self.client.initcol(col))

	def get_col(self, col):
		""" """
		return Col(col)

class Col(Client):
	def __init__(self, name):
		self.name = name
		self.path = os.path.join('data', self.name)

	def insert_one(self, doc):
		""" """
		self.client.initdoc(self.name, doc)

	def insert_many(self, docs):
		""" """
		for doc in docs:
			self.client.initdoc(self.name, doc)

	def update_one(self, query, docs):
		""" """
		if "_id" in docs:
			raise DenyEdit("Cannot edit _id.")
		gt = Query(self.path).load_one(query)
		if gt is None:
			raise NotFound("There was no document found with the provided query.")
		_id = gt["_id"]
		file = os.path.join(self.path, str(_id)+".json")

		self.client.updatedoc(file, docs)

	def update_many(self, query, docs):
		""" """
		if "_id" in docs:
			raise DenyEdit("Cannot edit _id.")
		gt_ = Query(self.path).load_filter(query)
		for gt in gt_:
			_id = gt["_id"]
			file = os.path.join(self.path, str(_id)+".json")

			self.client.updatedoc(file, docs)

	def update_all(self, docs):
		""" """
		for doc in docs:
			if "_id" in docs:
				raise DenyEdit("Cannot edit _id.")
		gt_ = Query(self.path).load_all()
		for gt in gt_:
			_id = gt["_id"]
			file = os.path.join(self.path, str(_id)+".json")

			self.client.updatedoc(file, docs)


	def find_all(self):
		""" """
		return Query(self.path).load_all()

	def find_many(self, query):
		""" """
		return Query(self.path).load_filter(query)

	def find_one(self, query):
		""" """
		return Query(self.path).load_one(query)

	def delete_one(self, query):
		""" """
		data = Query(self.path).load_one(query)
		if data is None:
			raise NotFound("There was no document found with the provided query.")
		os.remove(os.path.join(self.path, f"{data['_id']}.json"))

	def delete_many(self, query):
		""" """
		data_ = Query(self.path).load_filter(query)
		for data in data_:	
			os.remove(os.path.join(self.path, f"{data['_id']}.json"))

	def delete_all(self):
		""" """
		data_ = Query(self.path).load_all()
		for data in data_:	
			os.remove(os.path.join(self.path, f"{data['_id']}.json"))

	def drop(self):
		""" Deletes a collection """
		cn = os.listdir(self.path)
		if len(cn) == 0:
			os.rmdir(self.path)
		else:
			self.delete_all()
			cn2 = os.listdir(self.path)
			if len(cn2) == 0:
				os.rmdir(self.path)
			else:
				raise NotEmpty("The collection directory has foreign files. Please empty the directory to drop it.")

class Sort:
	def __init__(self, ls):
		self.ls = ls
		self.sorting = Sorting(self.ls)

	def by_asc(self, key):
		""" Sorts the list of dictionaries according to key in ascending order. """
		return self.sorting.by_asc(key)

	def by_desc(self, key):
		""" Sorts the list of dictionaries according to key in descending order. """
		return self.sorting.by_desc(key)