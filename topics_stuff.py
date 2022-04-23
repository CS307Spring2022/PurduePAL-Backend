import json
from typing import Tuple, List, Any

from bson import json_util

from helpers import db, safeget


def get_topics() -> list:
    topics_cursor = db["topics"].find()
    topics_dict = []
    for topic in topics_cursor:
        topic["_id"] = json_util.dumps(topic["_id"])
        for i in range(len(topic["posts"])):
            topic["posts"][i] = json.loads(json_util.dumps(topic["posts"][i]))
        topics_dict.append(topic)

    topics_dict = sorted(topics_dict, key=lambda x: len(x["posts"]) + len(x["usersFollowing"]), reverse=True)
    return topics_dict


def get_topic_posts(data: dict) -> Tuple[List[Any], bool]:
    user_id = safeget(data, "email", default="anonymous@purdue.edu")
    user = [u for u in db["users"].find({"_id": user_id})]
    if (len(user) == 0):
        return [{"val": "hi"}], False
    user = user[0]
    topic_name = safeget(data, "topic")

    likedPosts = [json.loads(json_util.dumps(post["post"]))["$oid"] for post in user["likedPosts"]]
    dislikedPosts = [json.loads(json_util.dumps(post["post"]))["$oid"] for post in user["dislikedPosts"]]
    savedPosts = [str(post) for post in user["savedPosts"]]

    posts_cursor = db["posts"].find({"topic": topic_name})
    posts_dict = []
    for post in posts_cursor:
        if (post["contentType"] == 0):
            post["_id"] = json.loads(json_util.dumps(post["_id"]))["$oid"]
            post["reactionType"] = 0
            post["isSaved"] = False
            if (post["_id"] in likedPosts):
                post["reactionType"] = 1
            elif (post["_id"] in dislikedPosts):
                post["reactionType"] = 2

            if (post['_id'] in savedPosts):
                post["isSaved"] = True

            if (post["parentID"]):
                post["parentID"] = json.loads(json_util.dumps(post["parentID"]))["$oid"]
            for i in range(len(post["comments"])):
                post["comments"][i] = json.loads(json_util.dumps(post["comments"][i]))["$oid"]
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