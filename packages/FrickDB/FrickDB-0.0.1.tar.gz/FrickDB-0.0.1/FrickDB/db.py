import json
from .exceptions import *
import os
import copy

class HandlerDir:
	def __init__(self):
		self.initclus()

	def initclus(self):
		dir = os.path.join("data")
		if not os.path.exists(dir):
			os.mkdir(dir)

	def initcol(self, col):
		if " " in col:
			raise BadName("Invalid character in provided collection name.")
		else:
			dir = os.path.join("data", col)
			if not os.path.exists(dir):
				os.mkdir(dir)
				return col
			else:
				raise DupExists("There is already a collection with the name.")

	def initdoc(self, col, doc):
		if " " in col:
			raise BadName("Invalid character in provided collection name.")
		else:
			if " " in doc:
				raise BadName("Invalid character in provided document name.")
			else:
				filedir = os.path.join("data", col)
				files = os.listdir(filedir)
				for file in files:
					if not file.endswith(".json"):
						files.pop(files.index(file))

				if "_id" not in doc:
					_id = f"doc_{len(files)}"
					doc["_id"] = _id
				else:
					_id = doc["_id"]

				dir = os.path.join("data", col, str(_id)+".json")
				if not os.path.exists(dir):
					file = open(dir, "w")
					json.dump(doc, file)
				else:
					raise DupExists("There is already a document with the name.")

	def updatedoc(self, file, doc):
		data = json.load(open(file, "r"))
		data.update(doc)
		json.dump(data, open(file, "w"))

class Sorting:
	def __init__(self, ls):
		self.ls = ls

	def by_asc(self, key):
		temp =  copy.copy(self.ls)
		least = None
		new = []
		
		for item in temp:
			if key not in item:
				temp.pop(temp.index(item))
		
		while len(temp) > 0:
			for item in temp:
				if least is None:
					least = item
				else:
					if type(least[key]) == type(item[key]):
						if least[key] > item[key]:
							least = item
					else:
						raise BadType("There are conflicting data types.")

			new.append(least)
			temp.pop(temp.index(least))
			least = None

		return new

	def by_desc(self, key):
		temp =  copy.copy(self.ls)
		least = None
		new = []
		
		for item in temp:
			if key not in item:
				temp.pop(temp.index(item))
		
		while len(temp) > 0:
			for item in temp:
				if least is None:
					least = item
				else:
					if type(least[key]) == type(item[key]):
						if least[key] < item[key]:
							least = item
					else:
						raise BadType("There are conflicting data types.")

			new.append(least)
			temp.pop(temp.index(least))
			least = None

		return new


class Query:
	def __init__(self, fp):
		self.fp = fp

	def load_all(self):
		files = os.listdir(self.fp)
		data = []
		for file in files:
			if not file.endswith(".json"):
				files.pop(files.index(file))

		for file in files:
			fn = file[:-5]
			path = os.path.join(self.fp, file)
			ret = json.load(open(path, "r"))
			data.append(ret)

		return data

	def load_filter(self, query):
		dump = self.load_all()
		for check in query.items():
			key = check[0]
			value = check[1]
			break

		data = []
		ret = []
		for item in dump:
			if key in item:
				if item[key] == value:
					data.append(item)

		return data

	def load_one(self, query):
		dump = self.load_all()
		for check in query.items():
			key = check[0]
			value = check[1]
			break

		for item in dump:
			if key in item:
				if item[key] == value:
					return item
		
