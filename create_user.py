from typing import Tuple
from helpers import safeget, db, check_for_data, encrypt_password
from userVerification import checkEmail, checkUsername, checkPasswordLength


def getUserInfo(data: dict) -> dict:
    if not check_for_data(data, "email"):
        return {}
    email = safeget(data, "email")
    info = db["users"].find_one({"_id": email})
    return info

def sign_up(data: dict) -> Tuple[int,str]:
    if not check_for_data(data, "firstName", "lastName", "email", "username", "password"):
        return (500,"missing data")
    first_name = safeget(data, "firstName")
    last_name = safeget(data, "lastName")
    email = safeget(data, "email")
    username = safeget(data, "username")
    password = safeget(data, "password")
    confirmPassword = safeget(data, "confirmPassword")
    if not password == confirmPassword:
        print("password")
        return (500,"conflicing passwords")
    if checkEmail(email) or checkUsername(username) or checkPasswordLength(password):  # verification errors
        print(email, username, password)
        return (500, "invalid lengths of fields")
    if db["users"].find_one({"_id": email}):
        return (400, "Email in Use!")
    if db["users"].find_one({"username": username}):
        return (400,"Username Taken! Please Choose Another.")
    return_val = db["users"].insert_one({"_id": email, "firstName": first_name, "lastName": last_name,
                                         "username": username, "password": encrypt_password(password)})
    if not return_val.acknowledged:
        print("huh")
        return (500, "mongodb error")
    return (200,"success")


def add_bio_to_user(data: dict, update_db: bool = True) -> bool:
    if not check_for_data(data, "email", "bio"):
        return False
    email = safeget(data, "email")
    bio = safeget(data, "bio")
    first_name = safeget(data, "firstName")
    last_name = safeget(data, "lastName")
    if len(bio) > 160:
        return False

    if update_db:
        stat = db["users"].update_one(filter={"_id": email}, update={"$set": {"bio": bio, "firstName": first_name, "lastName": last_name}})  # update user with email
        if stat.matched_count == 0:
            return False
    return True
