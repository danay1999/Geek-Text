from flask import Flask, render_template, jsonify, redirect, session, url_for, request, make_response
from six.moves.urllib.parse import urlencode
from functools import wraps
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
import pymongo
import requests
import json
import math

# Database
client = pymongo.MongoClient(
    "mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/test"
)
database = client["book_info"]
db_c = database["details"]
db = client.book_info

app = Flask(__name__, static_url_path="")
app.debug = True


@app.route("/")
def home():
    return render_template("/index.html")


@app.route("/login")
def login():
    return render_template("/login.html")


# from GeekText.views.index import bp as index_bp
# app.register_blueprint(index_bp)


@app.route("/wishlist", methods=["GET", "POST"])
def wishlist():

    results = db_c.find({}, {"book_name": 1, "author_name": 1})
    return render_template("wishlist.html", results=results)

@app.route("/books", methods=["GET"])
def books():
    try:
        books = db.details.find()
        return render_template("/books.html", books=books)
    except Exception as e:
        return dumps({"error": str(e)})


@app.route("/books/<link>", methods=["GET"])
def distinctbook(link):
    try:
        books = db.details.find()
        comments = db.details.find({"link" : link}, {"comment" : ""})
        rating = db.details.find({"link": link})
        count = 0
        sum = 0
        avg = 0
        for rate in rating: 
            for number in rate['avg_book_rating']:
               count+=1
               sum+=number
        avg=round(sum/count)
        db.details.update({"link": link}, {'$set' : {"avg" : avg}})
        return render_template("/distinctbooksandauthors/" + link + ".html", books=books, comments = comments, avg = avg)
    except Exception as e:
        return dumps({"error": str(e)})  


@app.route("/books/<link>/review", methods=['POST', 'GET'])
def message1(link):
    if request.method == 'POST' and request.get_json():
        rates = request.get_json(force=True)
        db.details.update({"link": link}, {'$push': {"avg_book_rating": rates }})
        res = make_response(jsonify({"message": "OK"}), 200)
        return res
    
    if request.method == 'POST' and request.form['comment']:
            comment = request.form['comment']
            if 'name' not in request.form:
                comments = db.details.update({"link": link}, {'$push': {"comment": "FirstName" + " : " + request.form.get('comment')}})
                return redirect("/books/"+link)
            else:
                if "Anonymous" in request.form['name']:
                    comments = db.details.update({"link": link}, {'$push': {"comment": "Anonymous" + " : " + request.form.get('comment')}})
                    return redirect("/books/"+link)
                else:
                    comments = db.details.update({"link": link}, {'$push': {"comment": "Nickname" + " : " + request.form.get('comment')}})
                    return redirect("/books/"+link)
    else:
            return render_template('/bookreviews/' + link + 'review.html')


        

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
