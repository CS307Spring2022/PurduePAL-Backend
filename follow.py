from helpers import safeget, db


def user_follow_topic(data):
    email = safeget(data, "email", default="anonymous@purdue.edu")
    topic = safeget(data, "topic")

    user = db["users"].find_one({"_id": email})

    if topic in user["topicsFollowing"]:
        return False, "User already following topic!"

    new_values = {"$push": {"topicsFollowing": topic}}
    # print(topic in user["topicsFollowing"])
    ret = db["users"].update_one({"_id": email}, new_values)
    # print(ret.acknowledged)
    if not ret.acknowledged:
        return False, "User Database Error!"

    ret = db["topics"].update_one({"_id": topic}, {"$push": {"usersFollowing": email}})
    if not ret.acknowledged:
        return False, "Topic Database Error!"

    return True, "Success!"


def get_followers(data):
    userId = safeget(data, "email")

    user_info = db["users"].find_one({"_id": userId})

    for i, user in enumerate(user_info["followingUsers"]):
        following_user_info = db["users"].find_one({"_id": user})
        user_info["followingUsers"][i] = {
            "name": following_user_info["firstName"] + " " + following_user_info["lastName"],
            "username": following_user_info["username"]
        }

    return True, {"msg": "Success!", "newFollowing": user_info["followingUsers"]}


def user_unfollow_topic(data):
    email = safeget(data, "email", default="anonymous@purdue.edu")
    topic = safeget(data, "topic")
    user = db["users"].find_one({"_id": email})
    if not user:
        return False, "User doesn't exist"

    if topic not in user["topicsFollowing"]:
        return False, "User already unfollowed topic!"

    new_values = {"$pull": {"topicsFollowing": topic}}
    # print(topic in user["topicsFollowing"])
    ret = db["users"].update_one({"_id": email}, new_values)
    # print(ret.acknowledged)
    if not ret.acknowledged:
        return False, "User Database Error!"

    ret = db["topics"].update_one({"_id": topic}, {"$pull": {"usersFollowing": email}})
    if not ret.acknowledged:
        return False, "Topic Database Error!"

    return True, "Success!"


def user1_follow_user2(user1id: str, user2id: str) -> bool:
    if user1id is None or user2id is None:
        return False
    if user1id == user2id:
        return False
    user1 = db["users"].find_one({"_id": user1id})
    user2 = db["users"].find_one({"_id": user2id})
    if not user1 or not user2:
        return False

    isPublic = user2["public"]

    if not isPublic:
        return False

    if user2id in user1["usersFollowing"]:
        return False
    # update user 1 following
    new_values = {"$push": {"usersFollowing": user2id}}
    ret = db["users"].update_one(user1, new_values)
    if ret.modified_count != 1:
        return False
    # update user2 followers
    new_values = {"$push": {"followingUsers": user1id}}
    if db["users"].update_one(user2, new_values).modified_count != 1:
        return False
    return True


def user1_unfollow_user2(user1id: str, user2id: str) -> bool:
    user1 = db["users"].find_one({"_id": user1id})
    user2 = db["users"].find_one({"_id": user2id})
    if not user1 or not user2:
        return False
    # update user 1 following
    new_values = {"$pull": {"usersFollowing": user2id}}
    if db["users"].update_one(user1, new_values).modified_count != 1:
        return False

    # update user2 followers
    new_values = {"$pull": {"followingUsers": user1id}}
    if db["users"].update_one(user2, new_values).modified_count != 1:
        return False
    return True
# def user_save_post(userID, postID):
# append post to savedPostsLine


# def user_comment_post(userID, postID)
# append to interactionsLine array


# post_liked():
# increment


# post_disliked():
# decrement
