import email
from email.message import EmailMessage
import pymongo
from helpers import safeget, db, check_for_data


def user_follow_topic(email: str, topicID):
    user = db["users"].find_one({"_id": email})
    new_values = {"$push": {"topicsFollowing": topicID}}

    db.update_one(user, new_values)

    # updating topics count

    # new_topics_count = user["topicsCount"] + 1
    # new_values = {"$set": {"topicsCount": new_topics_count}}
    # db.update_one(user, new_values)


def user_unfollow_topic(email: str, topicID):
    user = db["users"].find_one({"_id": email})
    new_values = {"$pull": {"topicsFollowing": topicID}}

    db.update_one(user, new_values)

    # updating topics count
    
    # new_topics_count = user["topicsCount"] - 1
    # new_values = {"$set": {"topicsCount": new_topics_count}}
    # db.update_one(user, new_values)


def user1_follow_user2(user1id: str, user2id: str) -> bool:
    user1 = db["users"].find_one({"_id": user1id})
    user2 = db["users"].find_one({"_id": user2id})

    isPublic = user2["public"]

    if not isPublic:
        return False

    # update user 1 following
    new_values = {"$push": {"following": user2id}}
    db.update_one(user1, new_values)

    # update user2 followers
    new_values = {"$push": {"followers": user1id}}
    db.update_one(user2, new_values)

    return True


def user1_unfollow_user2(user1id: str, user2id: str) -> bool:
    user1 = db["users"].find_one({"_id": user1id})
    user2 = db["users"].find_one({"_id": user2id})

    # update user 1 following
    new_values = {"$pull": {"following": user2id}}
    db.update_one(user1, new_values)

    # update user2 followers
    new_values = {"$pull": {"followers": user1id}}
    db.update_one(user2, new_values)

# def user_save_post(userID, postID):
# append post to savedPostsLine


# def user_comment_post(userID, postID)
# append to interactionsLine array


# post_liked():
# increment


# post_disliked():
# decrement
