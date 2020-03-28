from flask import Flask, render_template, jsonify, redirect, session, url_for, request
from six.moves.urllib.parse import urlencode
from functools import wraps
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
import pymongo
import requests
from flask_pymongo import PyMongo
import bcrypt


# Database
client = pymongo.MongoClient(
    "mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/test"
)
database = client["book_info"]
db_c = database["details"]
db = database["users"]
db_b = client.book_info

app = Flask(__name__, static_url_path="")

app.debug = True


@app.route("/")
def home():
    try:
        books = db_b.details.find()
        return render_template("/index.html", books=books)
    except Exception as e:
        return dumps({"error": str(e)})
    



# from GeekText.views.index import bp as index_bp
# app.register_blueprint(index_bp)


@app.route("/wishlist", methods=["GET", "POST"])
def wishlist():

    results = db_c.find({}, {"book_name": 1, "author_name": 1})
    return render_template("wishlist.html", results=results)

@app.route("/books", methods=["GET"])
def books():
    try:
        books = db_b.details.find()
        
        return render_template("/books.html", books=books)
    except Exception as e:
        return dumps({"error": str(e)})


@app.route("/books/<link>", methods=["GET"])
def distinctbook(link):
    try:
        books = db_b.details.find()
        authors = db_b.author.find()
        return render_template("/distinctbooksandauthors/" + link + ".html", books=books,  authors=authors)
    except Exception as e:
        return dumps({"error": str(e)})



@app.route("/shoppingcart")
def shoppingcart():
    return render_template("/shoppingcart.html")


app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/users'
mongo = PyMongo(app)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="localhost", port=env.get("PORT", 5000))


# Database functions
# Inserts data into the collection that you want
def insert_data(data):
    document = db_c.insert_one(data)
    return document.inserted_id


# Updates data or creates a new one if it doesn't have the same ID
def update_or_create(document_id, data):
    document = db_c.update_one(
        {"_id": ObjectId(document_id)}, {"$set": data}, upsert=True
    )
    return document.acknowledged


# Gets all the data of a single ID
def get_single_data(document_id):
    data = db_c.find_one({"_id": ObjectId(document_id)})
    return data


# Gets all the data inside the collection
def get_multiple_data():
    data = db_c.find()
    return list(data)


# Updates an existing data
def update_existing(document_id, data):
    document = db_c.update_one({"_id": ObjectId(document_id)}, {"$set": data})
    return document.acknowledged


# Removes the data
def remove_data(document_id):
    document = db_c.delete_one({"_id": ObjectId(document_id)})
    return document.acknowledged


# CLOSE DATABASE
client.close()
