import pymongo
import re

from error import Errors

def checkUsername(username):
	if len(username) > 13 or len(username) < 4:
		return Errors.USERNAME_ERROR
		print("Username must be between 4-13 characters long.")

	if not username.contains("[a-zA-Z0-9]*"):
		return Errors.USERNAME_ERROR
		print("Username can only contain alphanum characters")
	
	else:
		return

def checkEmail(email):
	if not email.contains("^\S+@purdue.edu$"):
		return Errors.EMAIL_ERROR
