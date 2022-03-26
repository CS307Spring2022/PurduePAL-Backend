import pymongo
import re
from helpers import check_password, safeget, db, check_for_data
from error import Errors


def checkUsername(username):
    if len(username) > 15 or len(username) < 4:
        return Errors.USERNAME_ERROR

    if not re.search("[a-zA-Z0-9]*", username):
        return Errors.USERNAME_ERROR

    else:
        return

def unique_user(data: dict, username: str):
    username_exists = db["users"].find_one(filter={"username": username})

    if username_exists:
        # username already exists
        return Errors.USERNAME_ERROR
    else:
        # username is unique, proceed with signup
        return True

>>>>>>> 5342c0acf7e898d8657b5497e096104362f1f33a


def checkEmail(email):
<<<<<<< HEAD
    if not re.search("^\S+@purdue.edu$", email):
        return Errors.EMAIL_ERROR


def checkPasswordLength(password):
    if len(password) < 8:
        return Errors.PASSWORD_ERROR


def confirmPassword(password, confirmation):
    if password != confirmation:
        return Errors.PASSWORD_ERROR
=======
    if not email.contains("^\S+@purdue.edu$"):
        return Errors.EMAIL_ERROR
        print("Please use a valid purdue.edu email.")


def checkPasswordLength(password):
    if len(password) < 8:
        return Errors.PASSWORD_ERROR
        print("Password must be at least 8 characters long.")


def confirmPassword(password, confirmation):
    if password != confirmation:
        return Errors.PASSWORD_ERROR
        print("Passwords don't match!")
>>>>>>> 5342c0acf7e898d8657b5497e096104362f1f33a
