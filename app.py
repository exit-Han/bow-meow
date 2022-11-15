from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os 
from pymongo import MongoClient
import certifi

ca = certifi.where()

# load .env
load_dotenv()

app = Flask(__name__)

client = MongoClient(os.environ.get('DB_URL'), tlsCAFile=ca)
db = client.sparta

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/details')
def detail():
    return render_template('details.html')

# 댓글기능
@app.route("/comments", methods=["POST"])
def comment_post():
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']

    doc = {
        'nickname': nickname_receive,
        'comment': comment_receive,
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '제보 완료!'})

@app.route("/comments", methods=["GET"])
def comment_get():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'lists':comment_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)