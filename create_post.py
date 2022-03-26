

from helpers import safeget, db


def create_post(data: dict) -> bool:
	
	topic = safeget(data, "topicName")
	user = safeget(data, "user")
	timestamp = safeget(data, "timestamp")
	likeCount = 0
	dislikeCount = 0
	isComment = False
	content = safeget(data, "content")
	comments = []
	commentCount = 0
	parent_id = safeget(data, "parentID")

	return_val = db["posts"].insert_one({"topic": topic, "user": user, "timestamp": timestamp, "likeCount": likeCount, "dislikeCount": dislikeCount,
	"isComment": isComment, "content": content, "comments": comments, "commentCount": commentCount, "parentID": parent_id})

	if not return_val.acknowledged:
		return False
	return True


#def create_comment()

