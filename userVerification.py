import re
from helpers import db
from error import Errors


def checkUsername(username):
    if len(username) > 15 or len(username) < 4:
        return Errors.USERNAME_ERROR

    if not re.search("[a-zA-Z0-9]*", username):
        return Errors.USERNAME_ERROR

    else:
        return


def unique_user(username: str):
    username_exists = db["users"].find_one(filter={"username": username})
    if username_exists:
        # username already exists
        return Errors.USERNAME_ERROR
    else:
        # username is unique, proceed with signup
        return True


def checkEmail(email):
    if not re.search(r"^\S+@purdue.edu$", email):
        return Errors.EMAIL_ERROR


def checkPasswordLength(password):
    if len(password) < 8:
        return Errors.PASSWORD_ERROR


def confirmPassword(password, confirmation):
    if password != confirmation:
        return Errors.PASSWORD_ERROR
