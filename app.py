from flask import Flask, request, jsonify
from flask_cors import CORS

from create_post import create_post, reactPost, save_post
from create_user import sign_up, add_bio_to_user, getUserInfo, save_profile_image, update_public
from delete_user_information import delete_post_from_db, delete_user_with_conf_code, delete_user_without_conf_code
from follow import user_follow_topic, user_unfollow_topic, user1_follow_user2, user1_unfollow_user2, get_followers
from helpers import safeget, db
from timeline import get_post_thread, get_timeline, saved_posts
from topics_stuff import get_topics, get_topic_posts
from userLogin import login

app = Flask(__name__)
CORS(app)


@app.route('/')  # default nonsense
def hello_world():
    return 'Hello World!'


@app.route('/followTopic', methods=['GET', 'POST'])
def followTopic():
    data = request.json
    success, msg = user_follow_topic(data)
    return_code = 200 if success else 400
    return jsonify({"message": msg}), return_code


@app.route('/unfollowTopic', methods=['GET', 'POST'])
def unfollowTopic():
    data = request.json
    success, msg = user_unfollow_topic(data)
    return_code = 200 if success else 400
    return jsonify({"message": msg}), return_code


@app.route('/followUser', methods=['POST'])
def follow_user():
    data = request.json
    user1 = safeget(data, "follower")
    user2 = safeget(data, "following")
    status = user1_follow_user2(user1, user2)
    return jsonify({"message": status})


@app.route('/unfollowUser', methods=['POST'])
def unfollow_user():
    data = request.json
    user1 = safeget(data, "follower")
    user2 = safeget(data, "following")
    if not user2:
        user2_username = safeget(data, "username")
        user2_obj = db["users"].find_one({"username": user2_username})
        if not user2_obj:
            return jsonify({"message": False})
        user2 = user2_obj["_id"]
    status = user1_unfollow_user2(user1, user2)
    return jsonify({"message": status})


@app.route('/getFollowers', methods=["POST"])
def getFollowers():
    data = request.json
    success, data = get_followers(data)
    return_code = 200 if success else 400
    return jsonify(data), return_code


@app.route('/topics', methods=['GET'])
def getTopics():
    topics = get_topics()
    return jsonify(topics)


@app.route('/topic_posts', methods=['GET'])
def getTopicPosts():
    data = request.args.to_dict()
    posts, success = get_topic_posts(data)
    if len(posts) > 0 and safeget(posts[0], "val"):
     posts[0]["logout"] = True
    status_code = 200 if success else 400
    return jsonify(posts), status_code


@app.route('/createPost', methods=['POST'])
def createPost():
    # file = request.files['profileImage']
    # data = request.form.get('data')
    data = request.json
    success,msg = create_post(data)
    return_code = 200 if success else 400
    return jsonify({msg: msg}),return_code


@app.route('/timeline', methods=['GET', 'POST'])
def getTimeline():
    data = request.json
    posts, success = get_timeline(data)
    if len(posts) > 0 and safeget(posts[0], "val"):
        posts[0]["logout"] = True
    status_code = 200 if success else 400
    return jsonify(posts), status_code


@app.route('/postThread', methods=['GET', 'POST'])
def getPostThread():
    data = request.json
    posts, success = get_post_thread(data)
    status_code = 200 if success else 400
    return jsonify(posts), status_code


@app.route('/getUser', methods=['GET', 'POST'])
def getUser():
    data = request.json
    user_data = getUserInfo(data)
    if safeget(user_data, "password"):
        user_data.pop("password")
    user_data["match"] = data["loggedUser"] == data["profileUser"]
    if (not user_data["public"]):
        return jsonify({"msg": "Profile is Private!"}), 200
    return jsonify(user_data), 200


@app.route('/sign_up', methods=['POST'])
def sign_up_process():
    data = request.json
    # created = sign_up(data)
    status_code, msg = sign_up(data)
    return jsonify({"return_code": status_code == 200, "msg": msg}), status_code


@app.route('/login', methods=['POST'])
def login_process():
    data = request.json
    loggedIn, email, username = login(data)
    status_code = 200 if loggedIn else 403
    return jsonify({"return_code": loggedIn, "email": email, "username": username}), status_code


@app.route('/updateUserInfo', methods=['POST'])
def add_bio():
    data = request.json
    # should contain email and bio
    added_bio = add_bio_to_user(data)
    status_code = 200 if added_bio else 403
    return jsonify({"return_code": added_bio}), status_code


@app.route('/updatePublic', methods=['POST'])
def make_private():
    data = request.json
    updated_public = update_public(data)
    status_code = 200 if updated_public else 403
    return jsonify({"return_code": updated_public}), status_code


@app.route('/delete_post', methods=['POST'])
def delete_post():
    data = request.json
    # should contain email and post id
    deleted_post = delete_post_from_db(data)
    return jsonify({"return_code": deleted_post})


@app.route('/delete_user', methods=['POST', 'GET'])
def delete_user():
    data = request.json
    other_data = request.args.to_dict()
    if safeget(other_data, "confirmation_code"):
        status = delete_user_with_conf_code(other_data)
    else:
        status = delete_user_with_conf_code(data)
    return jsonify({"no": status})


@app.route('/addProfileImage', methods=["POST"])
def addProfileImage():
    file = request.files['profileImage']
    email = request.form.get('email')
    ret = save_profile_image(file, email)
    return jsonify({"ret": ret})


@app.route('/interactPost', methods=["POST"])
def reactToPost():
    data = request.json
    val = reactPost(data)
    return jsonify({"return": val}), 200 if val else 400


@app.route('/savePost', methods=["POST"])
def savePost():
    data = request.json
    ret = save_post(data)
    return jsonify({"ret": ret}), 200 if ret else 400


@app.route('/savedPosts', methods=["POST"])
def savedPosts():
    data = request.json
    posts, status_code = saved_posts(data)
    status_code = 200 if status_code else 400
    return jsonify(posts), status_code



if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)
