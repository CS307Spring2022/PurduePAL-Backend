import json
from collections import defaultdict
from helpers import db
from bson import json_util


def get_topics() -> dict:
    topics_cursor = db["topics"].find()
    topics_dict = defaultdict()
    for topic in topics_cursor:
        topic["_id"] = json_util.dumps(topic["_id"])
        for i in range(len(topic["posts"])):
            topic["posts"][i] = json_util.dumps(topic["posts"][i])
        topics_dict[topic["topicName"]] = topic
    return topics_dict