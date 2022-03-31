import datetime
from typing import Tuple
from helpers import safeget, db
from bson import json_util
from json import loads


def get_timeline(data: dict) -> Tuple[list[dict],bool]:
    user_id = safeget(data,"email",default="anonymous@purdue.edu")
    user = [u for u in db["users"].find({"_id": user_id})]
    if (len(user) == 0):
        return [{"val": "hi"}],False
    user = user[0]
    users_following = user["usersFollowing"]
    topics_following = user["topicsFollowing"]

    posts_cursor = db["posts"].find({"topic":{"$in":topics_following}})

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

    return posts_dict,True