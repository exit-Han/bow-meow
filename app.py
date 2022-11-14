from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient("mongodb+srv://test:sparta@cluster0.hmoqxl5.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.dbsparta

print('hello')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)