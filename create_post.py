import datetime

from helpers import safeget, db


def update_parent_post(id_dict: dict, comment_id):
    db["posts"].update_one({"_id": id_dict}, {"$push": {"comments": comment_id}})
    db["posts"].update_one({"_id": id_dict}, {"$inc": {"commentCount": 1}})


def update_userline(user_id, isComment, timestamp, comment_id):
    db["users"].update_one(user_id, {
        "$push": {"userline": {"interactionType": int(isComment), "timestamp": timestamp, "post": comment_id}}})

    if (isComment):
        db["users"].update_one(user_id, {"$inc": {"responsePostCount": 1}})
    else:
        db["users"].update_one(user_id, {"$inc": {"originalPostCount": 1}})


def update_topic(topic_id_dict, user_id_dict, post_id):
    resp = db["topics"].find(topic_id_dict)
    resp_docs = [i for i in resp]
    resp_len = len(resp_docs)
    print(resp_len)

    if (resp_len == 0):
        add_ret = db["topics"].insert_one(
            {"_id": topic_id_dict["_id"], "posts": [], "postCount": 0, "usersFollowing": [], "followersCount": 0})
        print(add_ret.acknowledged)
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
    content_type = safeget(data, "contentType")
    content = safeget(data, "content")
    comments = []
    commentCount = 0
    parent_id = safeget(data, "parentID")
    isComment = (parent_id != None)

    return_val = db["posts"].insert_one(
        {"topic": topic, "user": user, "timestamp": timestamp, "likeCount": likeCount, "dislikeCount": dislikeCount,
         "isComment": isComment, "contentType": content_type, "content": content, "comments": comments,
         "commentCount": commentCount,
         "parentID": parent_id})

    if isComment:
        update_parent_post({"_id": parent_id}, return_val.inserted_id)

    update_userline({"_id": user}, isComment, timestamp, return_val.inserted_id)
    update_topic({"_id": topic}, {"_id": user}, return_val.inserted_id)

    if not return_val.acknowledged:
        return False
    return True


def reactPost(data: dict) -> bool:
    # 1: upvote, 2: downvote, 3: undo up, 4: undo down, 5: nothing happened
    if not safeget(data, "email") or not safeget(data, "postID"):
        return False
    interaction = {}
    postID = safeget(data, "postID")
    iv = data["interaction"]
    ret = False
    if iv == 1:
        interaction = {"$inc": {"likeCount": 1}}
        ret = db["users"].update_one({"_id": safeget(data, "email")}, {"$push": {"likedPosts": postID}}).acknowledged
    elif iv == 2:
        interaction = {"$inc": {"dislikeCount": 1}}
        ret = db["users"].update_one({"_id": safeget(data, "email")}, {"$push": {"dislikedPosts": postID}}).acknowledged
    elif iv == 3:
        interaction = {"$inc": {"likeCount": -1}}
        ret = db["users"].update_one({"_id": safeget(data, "email")}, {"$pull": {"likedPosts": postID}}).acknowledged
    elif iv == 4:
        interaction = {"$inc": {"dislikeCount": -1}}
        ret = db["users"].update_one({"_id": safeget(data, "email")}, {"$pull": {"dislikedPosts": postID}}).acknowledged
    elif iv == 5:
        ret = True
    if not db["posts"].update_one({"_id": data["postID"]}, interaction).acknowledged or not ret:
        return False
    return True

# def create_comment()
