import base64
from json import loads
from typing import Tuple

from bson import json_util

from helpers import safeget, db, check_for_data, encrypt_password
from userVerification import checkEmail, checkUsername, checkPasswordLength


def getUserInfo(data: dict) -> dict:
    if not check_for_data(data, "profileUser"):
        return {}
    user = safeget(data, "profileUser")
    info = db["users"].find_one({"username": user})
    for i in range(len(info["originalPosts"])):
        info["originalPosts"][i] = loads(json_util.dumps(info["originalPosts"][i]["post"]))
    for i in range(len(info["responsePosts"])):
        info["responsePosts"][i] = loads(json_util.dumps(info["responsePosts"][i]["post"]))
    for i in range(len(info["likedPosts"])):
        print(info["likedPosts"][i])
        info["likedPosts"][i] = loads(json_util.dumps(info["likedPosts"][i]["post"]))
    for i in range(len(info["dislikedPosts"])):
        info["dislikedPosts"][i] = loads(json_util.dumps(info["dislikedPosts"][i]["post"]))
    for i in range(len(info["savedPosts"])):
        info["savedPosts"][i] = loads(json_util.dumps(info["savedPosts"][i]["post"]))
    
    for i, user in enumerate(info["usersFollowing"]):
        user_info = db["users"].find_one({"_id": user})
        info["usersFollowing"][i] = {"name": user_info["firstName"] + " " + user_info["lastName"]}
    info["loggedFollows"] = False
    for i, user in enumerate(info["followingUsers"]):
        user_info = db["users"].find_one({"_id": user})
        if (user_info["_id"] == safeget(data, "loggedEmail")):
            info["loggedFollows"] = True
        info["followingUsers"][i] = {"name": user_info["firstName"] + " " + user_info["lastName"]}

    info["profilePic"] = str(info["profilePic"])
    info["profilePic"] = info["profilePic"][2:(len(info["profilePic"]) - 1)]
    info["profilePic"] = "data:image/png;base64," + info["profilePic"]

    return info


def sign_up(data: dict, testing=False) -> Tuple[int, str]:
    if not check_for_data(data, "firstName", "lastName", "email", "username", "password"):
        return 500, "missing data"
    first_name = safeget(data, "firstName")
    last_name = safeget(data, "lastName")
    email = safeget(data, "email")
    username = safeget(data, "username")
    password = safeget(data, "password")
    confirmPassword = safeget(data, "confirmPassword")
    if not password == confirmPassword:
        return 500, "conflicting passwords"
    if checkEmail(email) or checkUsername(username) or checkPasswordLength(password):  # verification errors
        return 500, "invalid lengths of fields"
    if db["users"].find_one({"_id": email}):
        return 400, "Email in Use!"
    if db["users"].find_one({"username": username}):
        return 400, "Username Taken! Please Choose Another."
    if not testing:
        return_val = db["users"].insert_one({"_id": email, "firstName": first_name, "lastName": last_name,
                                             "username": username, "password": encrypt_password(password),
                                             "public": True, "bio": "", "profilePic": "",
                                             "topicsFollowing": [], "usersFollowing": [], "followingUsers": [],
                                             "originalPosts": [], "responsePosts": [], "likedPosts": [], "dislikedPosts": [], "savedPosts": []})
        if not return_val.acknowledged:
            return 500, "mongodb error"
    return 200, "success"


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
        stat = db["users"].update_one(filter={"_id": email}, update={
            "$set": {"bio": bio, "firstName": first_name, "lastName": last_name}})  # update user with email
        if stat.matched_count == 0:
            return False
    return True


def save_profile_image(file, email) -> bool:
    encoded = base64.b64encode(file.read())
    ret = db["users"].update_one({"_id": email}, {"$set": {"profilePic": encoded}})
    if not ret.acknowledged:
        return False
    return True
