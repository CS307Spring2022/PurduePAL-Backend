import json

from bson import json_util

from helpers import db


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
