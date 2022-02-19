import os

from flask import Flask, request, jsonify
import pymongo

from create_user import sign_up

app = Flask(__name__)
db = pymongo.MongoClient(os.getenv("CONN"))

@app.route('/')  # default nonsense
def hello_world():
    return 'Hello World!'

@app.route('/sign_up', methods=['POST'])
def sign_up_process():
    data = request.json
    sign_up(data)
    return jsonify({"hi": "lol"})

if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)
