import os
import json

class Error(Exception):
	pass

class Message(Error):

    def __init__(self, message):
    	self.message = message

class BadName(Message):
    """Raised when database name is invalid"""
    pass

class DupExists(Message):
	"""Raised when a database already exists with the name"""
	pass

class NotEmpty(Message):
	"""Raised when a collection is not empty but attempted to delete"""
	pass

class DenyEdit(Message):
	"""Raised when user attempts to edit _id key"""
	pass

class NotFound(Message):
	""" Raised in update_one() when no document was found for the related query """
	pass

class BadType(Message):
	"""  """
	pass