import pymongo
import re
from helpers import check_password, safeget, db, check_for_data
from error import Errors


def checkUsername(username):
    if len(username) > 15 or len(username) < 4:
        return Errors.USERNAME_ERROR
        print("Username must be between 4-13 characters long.")

    if not username.contains("[a-zA-Z0-9]*"):
        return Errors.USERNAME_ERROR
        print("Username can only contain alphanum characters.")

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


def checkEmail(email):
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
