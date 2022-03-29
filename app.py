from flask import Flask, request, jsonify
from create_user import sign_up, add_bio_to_user, getUserInfo
from delete_user_information import delete_post_from_db, delete_user_with_conf_code, delete_user_without_conf_code
from helpers import safeget
from flask_cors import CORS

from userLogin import login

app = Flask(__name__)
CORS(app)


@app.route('/')  # default nonsense
def hello_world():
    return 'Hello World!'


@app.route('/getUser', methods=['GET'])
def getUser():
    data = request.args.to_dict()
    user_data = getUserInfo(data)
    if safeget(user_data, "profilePic"):
        user_data.pop("profilePic")
    return jsonify(user_data)


@app.route('/sign_up', methods=['POST'])
def sign_up_process():
    data = request.json
    # created = sign_up(data)
    status_code,msg = sign_up(data)

    return jsonify({"return_code": status_code==200,"msg": msg}), status_code


@app.route('/login', methods=['POST'])
def login_process():
    data = request.json
    loggedIn, email, username = login(data)
    status_code = 200 if loggedIn else 403
    return jsonify({"return_code": loggedIn, "email": email, "username": username}), status_code


@app.route('/update', methods=['POST'])
def add_bio():
    data = request.json
    # should contain email and bio
    added_bio = add_bio_to_user(data)
    status_code = 200 if added_bio else 403
    return jsonify({"return_code": added_bio}), status_code


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
        status = delete_user_without_conf_code(data)
    return jsonify({"no": status})


if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)
