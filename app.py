from flask import Flask, request, jsonify
from create_user import sign_up, add_bio_to_user

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

if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)
