from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
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


# 등록 페이지 렌더링
@app.route("/view/posts", methods=["GET"])
def posts_get():
    return render_template('post.html')


# 게시글 등록    
# [POST] /api/posts
@app.route("/api/posts", methods=["POST"])
def posts_post():
    params = request.get_json() # JSON형식으로 데이터를 받아온다
    basicInfo = params['basicInfo'] # 신고/제보 관련 기본 정보
    petInfo = params['petInfo'] # 신고/제보 관련 동물 정보

    try: 
        doc = {'basicInfo': basicInfo, 'petInfo': petInfo}
        db.posts.insert_one(doc) # 데이터 등록
    except:
        return jsonify({'msg': '등록에 실패하였습니다.'})
    else:
        return jsonify({'msg': '등록이 완료되었습니다.'})
    

# 게시글 리스트 조회
# GET /api/posts
@app.route("/api/posts", methods=["GET"])
def posts_list_get():
    page = list(db.posts.find({}))
    # TypeError: ObjectId('') is not JSON serializable 해결
    post_list = json.loads(json_util.dumps(page)) 
    
    return post_list


# 게시글 상세 조회
# GET /api/posts/:id
@app.route('/api/posts/<string:id>')
def detail(id):
    try:
        post = db.posts.find_one({'_id': ObjectId(id)})
        result = json.loads(json_util.dumps(post)) 
    except:
        return jsonify({'msg': '조회에 실패하였습니다.'})
    else:
        return render_template('details.html', data=result)


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

# 회원가입 페이지 렌더링
@app.route("/auth/join")
def join():
    return render_template('join.html')

# 로그인 페이지 렌더링
@app.route("/auth/login")
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)