from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os 

# load .env
load_dotenv()

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient(os.environ.get('DB_URL'))
db = client.dbsparta

# print('hello')

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)