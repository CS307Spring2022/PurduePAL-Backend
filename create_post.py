import datetime

from bson import ObjectId

from helpers import safeget, db


def update_parent_post(id_dict: dict, comment_id):
    print("hi",comment_id,id_dict)
    db["posts"].update_one(id_dict, {"$push": {"comments": ObjectId(comment_id)}})
    db["posts"].update_one(id_dict, {"$inc": {"commentCount": 1}})


def update_userline(user_id, isComment, timestamp, comment_id):
    if (isComment):
        db["users"].update_one(user_id, {
        "$push": {"responsePosts": {"post": comment_id, "timestamp": timestamp}}})
    else:
       db["users"].update_one(user_id, {
        "$push": {"originalPosts": {"post": comment_id, "timestamp": timestamp}}})


def update_topic(topic_id_dict, user_id_dict, post_id):
    resp = db["topics"].find(topic_id_dict)
    resp_docs = [i for i in resp]
    resp_len = len(resp_docs)
    # print(resp_len)

    if (resp_len == 0):
        print(topic_id_dict)
        add_ret = db["topics"].insert_one(
            {"_id": str(topic_id_dict["_id"]), "posts": [], "postCount": 0, "usersFollowing": [], "followersCount": 0})
        # print(add_ret.acknowledged)
    else:
        print(resp_docs)

    db["topics"].update_one(topic_id_dict, {"$push": {"posts": post_id}})
    db["topics"].update_one(topic_id_dict, {"$inc": {"postCount": 1}})

    user_topics = db["users"].find_one(user_id_dict)["topicsFollowing"]
    if (topic_id_dict["_id"] not in user_topics):
        db["users"].update_one(user_id_dict, {"$push": {"topicsFollowing": topic_id_dict["_id"]}})
        db["topics"].update_one(topic_id_dict, {"$push": {"usersFollowing": user_id_dict["_id"]}})
        db["topics"].update_one(topic_id_dict, {"$inc": {"followersCount": 1}})


def create_post(data: dict) -> bool:
    # print(data)
    topic = safeget(data, "topicName")
    user = safeget(data, "user", default="anonymous@purdue.edu")
    # print(user)
    timestamp = datetime.datetime.utcnow().isoformat()
    likeCount = 0
    dislikeCount = 0
    savedCount = 0
    content_type = safeget(data, "contentType")
    content = safeget(data, "content")
    # print(safeget(data,"postImage"))
    img = safeget(data,"postImage")
    comments = []
    commentCount = 0
    parent_id = safeget(data, "parentID")
    if parent_id != None:
        parent_id = ObjectId(parent_id)
    isComment = (parent_id != None)

    return_val = db["posts"].insert_one(
        {"topic": topic, "user": user, "timestamp": timestamp, "likeCount": likeCount, "dislikeCount": dislikeCount,
         "isComment": isComment, "contentType": content_type, "content": content, "comments": comments, "savedCount": savedCount,
         "commentCount": commentCount, "img": None if (img=="") else img,
         "parentID": parent_id})

    if not return_val.acknowledged:
        return False,"Fail"

    if isComment:
        update_parent_post({"_id": parent_id}, return_val.inserted_id)

    update_userline({"_id": user}, isComment, timestamp, return_val.inserted_id)
    update_topic({"_id": topic}, {"_id": user}, return_val.inserted_id)


    return True,"Success"


def reactPost(data: dict) -> bool:
    # 1: upvote, 2: downvote, 3: undo up, 4: undo down, 5: nothing happened
    if not safeget(data, "email") or not safeget(data, "postID"):
        return False
    interaction = {}
    postID = ObjectId(safeget(data, "postID"))
    email = safeget(data, "email")
    iv = data["interaction"]
    ret = False
    if iv == 1:
        interaction = {"$inc": {"likeCount": 1}}
        ret = db["users"].update_one({"_id": email}, {"$push": {"likedPosts": {"post":postID,"timestamp":datetime.datetime.utcnow().isoformat()}}}).acknowledged
        if db["users"].update_one({"_id": email}, {"$pull": {"dislikedPosts": {"post":postID}}}).modified_count != 0:
            interaction["$inc"]["dislikeCount"] = -1
    elif iv == 2:
        interaction = {"$inc": {"dislikeCount": 1}}
        ret = db["users"].update_one({"_id": email}, {"$push": {"dislikedPosts": {"post":postID,"timestamp":datetime.datetime.utcnow().isoformat()}}}).acknowledged
        if db["users"].update_one({"_id": email}, {"$pull": {"likedPosts": {"post":postID}}}).modified_count != 0:
            interaction["$inc"]["likeCount"] = -1
    elif iv == 3:
        interaction = {"$inc": {"likeCount": -1}}
        ret = db["users"].update_one({"_id": email}, {"$pull": {"likedPosts": {"post":postID}}}).acknowledged
    elif iv == 4:
        interaction = {"$inc": {"dislikeCount": -1}}
        ret = db["users"].update_one({"_id": email}, {"$pull": {"dislikedPosts": {"post":postID}}}).acknowledged
    elif iv == 5:
        ret = True
    if iv != 5:
        if db["posts"].update_one({"_id": postID}, interaction).modified_count != 1 or not ret:
            return False
    return True


def save_post(data):
    if not safeget(data, "postID") or not safeget(data, "email"):
        return False
    savedPostID = {
        "post": ObjectId(safeget(data, "postID"))
    }
    if db["users"].update_one({"_id": safeget(data, "email")},
                              {"$pull": {"savedPosts": savedPostID}}).modified_count == 1:
        return True
    if db["users"].update_one({"_id": safeget(data, "email")},
                              {"$push": {"savedPosts": savedPostID}}).modified_count != 1:
        return False
    return True
