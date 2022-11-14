from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://yujin:*RpiZ99tUSxr8UR@cluster0.s5ahq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# print('hello')

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)