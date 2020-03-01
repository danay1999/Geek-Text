from flask import Flask, render_template, jsonify, redirect, session, url_for
from six.moves.urllib.parse import urlencode
from functools import wraps
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
import pymongo
import requests
import json
import constants

# Database
client = pymongo.MongoClient("mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/test")
database = client["book_info"]
db_c = database["details"]
db = client.book_info



app = Flask(__name__, static_url_path="")
app.secret_key = constants.SECRET_KEY
app.debug = True



@app.route("/")
def home():
    return render_template("/index.html")


@app.route("/login")
def login():
    return render_template("/login.html")
    


# from GeekText.views.index import bp as index_bp
# app.register_blueprint(index_bp)

@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():

    results = db_c.find({}, {"book_name": 1, "author_name": 1})
    return render_template('wishlist.html', results=results)

@app.route("/books", methods = ['GET'])
def books():
    try:
        books = db.details.find()
        return render_template("/books.html", books=books)
    except Exception as e:
        return dumps({'error' : str(e)})


@app.route("/books/<link>")
def distinctbook(link):
    return render_template("/distinctbooks/"+link+".html",books=books)


@app.route("/shoppingcart")
def shoppingcart():
    return render_template("/shoppingcart.html")


@app.route("/signup")
def signup():
    return render_template("/signup.html")

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
    document = db_c.update_one({'_id': ObjectId(document_id)}, {"$set": data}, upsert=True)
    return document.acknowledged

# Gets all the data of a single ID
def get_single_data(document_id):
    data = db_c.find_one({'_id': ObjectId(document_id)})
    return data

# Gets all the data inside the collection
def get_multiple_data():
    data = db_c.find()
    return list(data)

# Updates an existing data
def update_existing(document_id, data):
    document = db_c.update_one({'_id': ObjectId(document_id)}, {"$set": data})
    return document.acknowledged

# Removes the data
def remove_data(document_id):
    document = db_c.delete_one({'_id': ObjectId(document_id)})
    return document.acknowledged


# CLOSE DATABASE
client.close()