import os

from flask import Flask
import pymongo

app = Flask(__name__)
db = pymongo.MongoClient(os.getenv("CONN"))
# print(db["admin"])

@app.route('/')  # default nonsense
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)
