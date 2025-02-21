from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os 
from pymongo import MongoClient


import jwt
import datetime
import hashlib

import certifi

ca = certifi.where()
client = MongoClient("mongodb+srv://yujin:*RpiZ99tUSxr8UR@cluster0.s5ahq.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dbsparta_plus_week4

SECRET_KEY = 'SPARTA'

# load .env
load_dotenv()

app = Flask(__name__)

client = MongoClient(os.environ.get('DB_URL'))
db = client.sparta
#
# @app.route('/')
# def home():
#     return render_template('main.html')
#
# @app.route('/details')
# def detail():
#     return render_template('details.html')
#

@app.route('/')
def login():
    return render_template('login.html')


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.form['email']
    passward = request.form['passward']


    pw_hash = hashlib.sha256(passward.encode('utf-8')).hexdigest()

    # email, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'email': email, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
# @app.route('/api/nick', methods=['GET'])
#
# def api_valid():
#     token_receive = request.cookies.get('mytoken')
#
#     # try / catch 문?
#     # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.
#
#     try:
#         # token을 시크릿키로 디코딩합니다.
#         # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         print(payload)
#
#         # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
#         # 여기에선 그 예로 닉네임을 보내주겠습니다.
#         userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
#         return jsonify({'result': 'success', 'nickname': userinfo['nick']})
#     except jwt.ExpiredSignatureError:
#         # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
#         return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
#     except jwt.exceptions.DecodeError:
#         return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
#

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)