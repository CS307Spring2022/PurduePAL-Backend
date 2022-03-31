from json import loads
from typing import Tuple, List

from bson import json_util

from helpers import safeget, db


def get_timeline(data: dict) -> Tuple[List[dict], bool]:
    user_id = safeget(data, "email", default="anonymous@purdue.edu")
    user = [u for u in db["users"].find({"_id": user_id})]
    if (len(user) == 0):
        return [{"val": "hi"}], False
    user = user[0]
    users_following = user["usersFollowing"]
    topics_following = user["topicsFollowing"]

    posts_cursor = db["posts"].find({"topic": {"$in": topics_following}})

    posts_dict = []
    for post in posts_cursor:
        if (post["contentType"] == 0):
            post["_id"] = loads(json_util.dumps(post["_id"]))["$oid"]
            if (post["parentID"]):
                post["parentID"] = loads(json_util.dumps(post["parentID"]))["$oid"]
            for i in range(len(post["comments"])):
                post["comments"][i] = loads(json_util.dumps(post["comments"][i]))["$oid"]
            posts_dict.append(post)

            poster = [u for u in db["users"].find({"_id": post["user"]})][0]
            poster = {
                "username": poster["username"],
                "email": poster["_id"],
                "firstName": poster["firstName"],
                "lastName": poster["lastName"],
                "public": poster["public"]
            }
            post["user"] = poster

    return posts_dict, True


def saved_posts(data) -> Tuple[List[dict], bool]:
    if not safeget(data, "email"):
        return [{"val": "hi"}], False
    saved_ids = db["users"].find_one({"_id": safeget(data, "email")})["savedPosts"]
    posts_cursor = db["posts"].find({"_id": {"$in": saved_ids}})

    posts_dict = []
    for post in posts_cursor:
        if (post["contentType"] == 0):
            post["_id"] = loads(json_util.dumps(post["_id"]))["$oid"]
            if (post["parentID"]):
                post["parentID"] = loads(json_util.dumps(post["parentID"]))["$oid"]
            for i in range(len(post["comments"])):
                post["comments"][i] = loads(json_util.dumps(post["comments"][i]))["$oid"]
            posts_dict.append(post)

            poster = [u for u in db["users"].find({"_id": post["user"]})][0]
            poster = {
                "username": poster["username"],
                "email": poster["_id"],
                "firstName": poster["firstName"],
                "lastName": poster["lastName"],
                "public": poster["public"]
            }
            post["user"] = poster

    return posts_dict, True
