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

def checkPasswordLength(password):
	if len(password) < 8:
		return Errors.PASSWORD_ERROR
		print("Password must be at least 8 characters long")

def confirmPassword(password, confirmation):
	if password != confirmation:
		return Errors.PASSWORD_ERROR
		print("Passwords don't match")
