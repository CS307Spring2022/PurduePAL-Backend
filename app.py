from flask import Flask, request, jsonify
from create_user import sign_up, add_bio_to_user
from delete_user_information import delete_post_from_db, delete_user_with_conf_code, delete_user_without_conf_code
from helpers import safeget

app = Flask(__name__)

@app.route('/')  # default nonsense
def hello_world():
    return 'Hello World!'


@app.route('/sign_up', methods=['POST'])
def sign_up_process():
    data = request.json
    created = sign_up(data)
    return jsonify({"return_code": created})


@app.route('/add_bio', methods=['POST'])
def add_bio():
    data = request.json
    # should contain email and bio
    added_bio = add_bio_to_user(data)
    return jsonify({"return_code": added_bio})


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
        if status:
            return "Account Deleted"
        else:
            return "Please try again"
    else:
        status = delete_user_without_conf_code(data)
        return jsonify({"return_code": status}), status


if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)
