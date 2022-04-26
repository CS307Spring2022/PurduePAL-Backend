from json import loads
from typing import Tuple, List

from bson import json_util, ObjectId

from helpers import safeget, db


def get_timeline(data: dict) -> Tuple[List[dict], bool]:
    user_id = safeget(data, "email", default="anonymous@purdue.edu")
    user = [u for u in db["users"].find({"_id": user_id})]
    if (len(user) == 0):
        return [{"val": "hi"}], False
    user = user[0]
    users_following = user["usersFollowing"]
    topics_following = user["topicsFollowing"]

    likedPosts = [loads(json_util.dumps(post["post"]))["$oid"] for post in user["likedPosts"]]
    dislikedPosts = [loads(json_util.dumps(post["post"]))["$oid"] for post in user["dislikedPosts"]]
    savedPosts = [str(post) for post in user["savedPosts"]]

    # print(likedPosts)

    posts_cursor = db["posts"].find({"topic": {"$in": topics_following}})

    posts_dict = []
    for post in posts_cursor:
        post["_id"] = loads(json_util.dumps(post["_id"]))["$oid"]
        post["reactionType"] = 0
        post["isSaved"] = False
        if (post["_id"] in likedPosts):
            post["reactionType"] = 1
        elif (post["_id"] in dislikedPosts):
            post["reactionType"] = 2
        
        if (post['_id'] in savedPosts):
            post["isSaved"] = True

        if (post["parentID"]):
            post["parentID"] = loads(json_util.dumps(post["parentID"]))["$oid"]
            parentPost = db["posts"].find_one({"_id": ObjectId(post["parentID"])})
            # print(parentPost)
            parentPoster = [u for u in db["users"].find({"_id": parentPost["user"]})][0]
            parentPoster = {
                "username": parentPoster["username"],
                "email": parentPoster["_id"],
                "firstName": parentPoster["firstName"],
                "lastName": parentPoster["lastName"],
                "public": parentPoster["public"]
            }
            post["parentUser"] = parentPoster["username"]
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
    saved_ids = [saved_id["post"] for saved_id in saved_ids]
    posts_cursor = db["posts"].find({"_id": {"$in": saved_ids}})

    posts_dict = []
    for post in posts_cursor:
        post["_id"] = loads(json_util.dumps(post["_id"]))["$oid"]
        if (post["parentID"]):
            post["parentID"] = loads(json_util.dumps(post["parentID"]))["$oid"]
            parentPost = db["posts"].find_one({"_id": ObjectId(post["parentID"])})
            # print(parentPost)
            parentPoster = [u for u in db["users"].find({"_id": parentPost["user"]})][0]
            parentPoster = {
                "username": parentPoster["username"],
                "email": parentPoster["_id"],
                "firstName": parentPoster["firstName"],
                "lastName": parentPoster["lastName"],
                "public": parentPoster["public"]
            }
            post["parentUser"] = parentPoster["username"]

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
        post["isSaved"] = True
        post["user"] = poster

    return posts_dict, True


def get_post_thread(data):
    user_id = safeget(data, "email", default="anonymous@purdue.edu")
    post_id = safeget(data,"postId")
    ret_dict = {}

    user = [u for u in db["users"].find({"_id": user_id})]
    if (len(user) == 0):
        return [{"val": "hi"}], False
    user = user[0]

    users_following = user["usersFollowing"]
    topics_following = user["topicsFollowing"]

    parentPost = db["posts"].find_one({"_id": ObjectId(post_id)})
    
    likedPosts = [loads(json_util.dumps(post["post"]))["$oid"] for post in user["likedPosts"]]
    dislikedPosts = [loads(json_util.dumps(post["post"]))["$oid"] for post in user["dislikedPosts"]]
    savedPosts = [str(post) for post in user["savedPosts"]]

    parentPost["_id"] = loads(json_util.dumps(parentPost["_id"]))["$oid"]
    parentPost["reactionType"] = 0
    parentPost["isSaved"] = False
    if (str(parentPost["_id"]) in likedPosts):
        parentPost["reactionType"] = 1
    elif (str(parentPost["_id"]) in dislikedPosts):
        parentPost["reactionType"] = 2
    
    if (str(parentPost['_id']) in savedPosts):
        parentPost["isSaved"] = True

    if (parentPost["parentID"]):
        parentPost["parentID"] = loads(json_util.dumps(parentPost["parentID"]))["$oid"]
        parentParentPost = db["posts"].find_one({"_id": ObjectId(parentPost["parentID"])})
        # print(parentPost)
        parentPoster = [u for u in db["users"].find({"_id": parentParentPost["user"]})][0]
        parentPoster = {
            "username": parentPoster["username"],
            "email": parentPoster["_id"],
            "firstName": parentPoster["firstName"],
            "lastName": parentPoster["lastName"],
            "public": parentPoster["public"]
        }
        print(parentPoster["username"])
        parentPost["parentUser"] = parentPoster["username"]

    for i in range(len(parentPost["comments"])):
        parentPost["comments"][i] = loads(json_util.dumps(parentPost["comments"][i]))["$oid"]

    poster = [u for u in db["users"].find({"_id": parentPost["user"]})][0]
    poster = {
        "username": poster["username"],
        "email": poster["_id"],
        "firstName": poster["firstName"],
        "lastName": poster["lastName"],
        "public": poster["public"]
    }
    parentPost["user"] = poster

    ret_dict["parentPost"] = parentPost

    likedPosts = [loads(json_util.dumps(post["post"]))["$oid"] for post in user["likedPosts"]]
    dislikedPosts = [loads(json_util.dumps(post["post"]))["$oid"] for post in user["dislikedPosts"]]
    savedPosts = [str(post) for post in user["savedPosts"]]


    posts_dict = []
    for comment in parentPost["comments"]:
        # print(comment)
        post = db["posts"].find_one({"_id":ObjectId(comment)})
        # print(post)
        post["_id"] = loads(json_util.dumps(post["_id"]))["$oid"]
        post["reactionType"] = 0
        post["isSaved"] = False
        if (post["_id"] in likedPosts):
            post["reactionType"] = 1
        elif (post["_id"] in dislikedPosts):
            post["reactionType"] = 2
        
        if (post['_id'] in savedPosts):
            post["isSaved"] = True

        if (post["parentID"]):
            post["parentID"] = loads(json_util.dumps(post["parentID"]))["$oid"]
            parentPost = db["posts"].find_one({"_id": ObjectId(post["parentID"])})
            # print(parentPost)
            parentPoster = [u for u in db["users"].find({"_id": parentPost["user"]})][0]
            parentPoster = {
                "username": parentPoster["username"],
                "email": parentPoster["_id"],
                "firstName": parentPoster["firstName"],
                "lastName": parentPoster["lastName"],
                "public": parentPoster["public"]
            }
            post["parentUser"] = parentPoster["username"]
        for i in range(len(post["comments"])):
            post["comments"][i] = loads(json_util.dumps(post["comments"][i]))["$oid"]

        poster = [u for u in db["users"].find({"_id": post["user"]})][0]
        poster = {
            "username": poster["username"],
            "email": poster["_id"],
            "firstName": poster["firstName"],
            "lastName": poster["lastName"],
            "public": poster["public"]
        }
        post["user"] = poster
        posts_dict.append(post)

    ret_dict["comments"] = posts_dict

    return ret_dict, True