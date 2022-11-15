from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

# load .env
load_dotenv()

app = Flask(__name__)

client = MongoClient(os.environ.get('DB_URL'))
db = client.sparta

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/details')
def detail():
    return render_template('details.html')

# 등록 페이지 렌더링
@app.route("/view/posts", methods=["GET"])
def posts_get():
    return render_template('post.html')
    
# [POST] /api/posts
# {
#   'id': post_id,
#   'basicInfo': {
#     'type': type,
#     'date': date,
#     'location': location,
#     'tel': tel
#   },
#   'petInfo': {
#     'type': type,
#     'sex': sex,
#     'age': age,
#     'weight': weight,
#     'feature': feature,
#     'detail': detail
#   }
# }
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
    

# GET /api/posts
@app.route("/api/posts", methods=["GET"])
def posts_list_get():
    page = list(db.posts.find({}))
    # TypeError: ObjectId('') is not JSON serializable 해결
    post_list = json.loads(json_util.dumps(page)) 
    
    return post_list


# GET /api/posts/:id
@app.route("/api/posts/<string:id>", methods=["GET"])
def posts_read_get(id):
    params = request.get_json() 
    id = params['id']  # 등록된 post의 id

    try:
        post = db.posts.find_one({'_id': ObjectId(id)})
        result = json.loads(json_util.dumps(post)) 
    except:
        return jsonify({'msg': '조회에 실패하였습니다.'})
    else:
        return jsonify(result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)