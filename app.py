from flask import Flask, render_template, request, jsonify
from flask_restx import Resource, Api
from dotenv import load_dotenv
import os 
from pymongo import MongoClient
from controller.test import Test as test_ns;

# load .env
load_dotenv()

# DB 연결
# client = MongoClient(os.environ.get('DB_URL'))
# db = client.dbsparta



# Flask 객체에 Api 객체 등록
# 아래와 같이, version, title, description... 등의 내용들을 추가해서 넣어줄 수 있다.
def create_env(): 
    app = Flask(__name__)
    api = Api(
                app,
                version='0.1',
                title="BOW-MEOW API Server",
                description="BOW-MEOW API Server!",
                terms_url="/"
    )

    # 이 파일이 아닌 외부에 있는 파일에 클래스를 구현하고 
    # 여기서 import한 다음 add_resource()를 통해 클래스를 등록
    api.add_namespace(test_ns, '/test') # namespace에서 url 들어갈 부분 머로 들어가는지 확인해야함 => 여기선 /test

    return app