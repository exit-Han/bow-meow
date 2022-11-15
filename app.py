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



# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################



@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        "userId": id_receive,  # 아이디
        "password": pw_hash,  # 비밀번호
        "nickname": nickname_receive  # 닉네임
    }

    db.user.insert_one(doc)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)