from flask import Flask, render_template, jsonify
from GeekText.views.index import bp as index_bp
import requests
import json

app = Flask(__name__)

app.register_blueprint(index_bp)

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/wishlist')
def wishlist():
    return render_template('/wishlist.html')

@app.route('/shoppingcart')
def shoppingcart():
    return render_template('/shoppingcart.html')

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/signup')
def signup():
    return render_template('/signup.html')

if __name__ == '__main__':
    app.run(debug=True)

