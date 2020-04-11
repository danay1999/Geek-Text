from flask import Flask, render_template, jsonify, redirect, session, url_for, request , flash, make_response
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
from bson import ObjectId
from bson.json_util import dumps
from forms import TitleForm1, TitleForm2, TitleForm3
import os
from flask_login import login_user


# Database
client = pymongo.MongoClient(
    "mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/test"
)
database = client["book_info"]
db_c = database["details"]
wishlist_c = database['wish_list']  # wishlist collection.
cart_c= database['shopping_cart']
save_c= database['save_for_later']
db_b = client.book_info
db_u = database["users"]
db_ch = database["cards"]
db_a = database["address"]
app = Flask(__name__, static_url_path="")
app.debug = True

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/")
def home():
    return render_template("/index.html")
 
# from GeekText.views.index import bp as index_bp
# app.register_blueprint(index_bp)



@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    print("WISHLIST")
    form1 = TitleForm1()
    form2 = TitleForm2()
    form3 = TitleForm3()
    if form1.validate_on_submit():
        flash(f'Titles Created Successfully! : {form1.title1.data}','success')
        wishlist_c.update_one({"wishlist_id":1},{"$set":{"wishlist_title": form1.title1.data}})
        return redirect(url_for('wishlist'))

    if form2.validate_on_submit():
        flash(f'Titles Created Successfully! :  {form2.title2.data}','success')
        wishlist_c.update_one({"wishlist_id":2},{"$set":{"wishlist_title2": form2.title2.data}})
        return redirect(url_for('wishlist'))

    if form3.validate_on_submit():
        flash(f'Titles Created Successfully! :  {form3.title3.data}','success')
        wishlist_c.update_one({"wishlist_id":3},{"$set":{"wishlist_title3": form3.title3.data}})
        return redirect(url_for('wishlist'))


    # This needs to pass eventually the wishlist collection and not the books db_c
    # results = wishlist_c.find(
    #     {}, {"_id": 1, "wishlist_title": 1, "books_arr": 1, "wishlist_id":1})
    results = wishlist_c.find({"wishlist_id": 1})
    results2 = wishlist_c.find(
        {}, {"_id": 1, "wishlist_title2": 1, "books_arr2": 1,"wishlist_id":1})

    results3 = wishlist_c.find(
        {}, {"_id": 1, "wishlist_title3": 1, "books_arr3": 1, "wishlist_id":1})

    return render_template('wishlist.html', results=results, results2=results2, results3=results3, form1=form1, form2=form2,form3=form3)

###########################################################
#Wish list add btn.
@app.route("/add/<list_id>/<book_id>")
def add(list_id,book_id):
    # Add a wishlist item.
    print("ADDED")
    print("LIST NUMBER: ",list_id )
    print("BOOK ID: ",book_id)

    # key = request.values.get("_id")
    # print(key)
    result = db_c.find_one({"_id": ObjectId(book_id)})
    # wishlist_c.update_one({"wishlist_id": 1}, {
    #                       "$push": {"books_arr": ObjectId(key)}})
    # print("PRINTING RESULT: ", result)
    if list_id == "1":
        wishlist_c.update_one({"wishlist_id": 1}, {
                          "$addToSet": {"books_arr": result}})
    elif list_id == "2":
        wishlist_c.update_one({"wishlist_id": 2}, {
                          "$addToSet": {"books_arr2": result}})
    else:
        wishlist_c.update_one({"wishlist_id": 3}, {
                          "$addToSet": {"books_arr3": result}})




    # wishlist_c.update_one({"wishlist_id": 1}, {
                        #   "$addToSet": {"books_arr": result}})
    # wishlist_c.insert_one(result)
    return redirect('/books')
###########################################################
# Wishlist remove btn.
@app.route("/remove/<list_id>/<book_id>")
def remove(list_id, book_id):
    # Delete wishlist item.
    print("REMOVED")
    # key = request.values.get("_id")

    # key = request.values.get("_id")

    # if list_id == "1":

    # wishlist_c.delete_one({"books_arr": key})

    if list_id == "1":
         wishlist_c.update_one({"wishlist_id": 1}, {
                          "$pull": {"books_arr": {"_id": ObjectId(book_id)}}})
    elif list_id == "2":
         wishlist_c.update_one({"wishlist_id": 2}, {
                          "$pull": {"books_arr2": {"_id": ObjectId(book_id)}}})
    else:
         wishlist_c.update_one({"wishlist_id": 3}, {
                          "$pull": {"books_arr3": {"_id": ObjectId(book_id)}}})


   
    return redirect('/wishlist')
######################################################################
# Wishlist move btn
@app.route("/moveBooks/<list_id>/<book_id>")
def moveBooks(list_id, book_id):
    
    if list_id == "1":
        print("LIST ID: ", list_id)
        #Add to 2nd Array of Books
        result = db_c.find_one({"_id": ObjectId(book_id)})
        wishlist_c.update_one({"wishlist_id": 2}, {
                          "$addToSet": {"books_arr2": result}})
        #Remove from 1st Array of Books
        wishlist_c.update_one({"wishlist_id": 1}, {
                          "$pull": {"books_arr": {"_id":ObjectId(book_id)}}})
    elif list_id == "2":
        result = db_c.find_one({"_id": ObjectId(book_id)})
        wishlist_c.update_one({"wishlist_id": 3}, {
                          "$addToSet": {"books_arr3": result}})
        wishlist_c.update_one({"wishlist_id": 2}, {
                          "$pull": {"books_arr2": {"_id":ObjectId(book_id)}}})
    else:
        result = db_c.find_one({"_id": ObjectId(book_id)})
        wishlist_c.update_one({"wishlist_id": 1}, {
                          "$addToSet": {"books_arr": result}})
        wishlist_c.update_one({"wishlist_id": 3}, {
                          "$pull": {"books_arr3": {"_id":ObjectId(book_id)}}})

    # print("BOOK ID: ", book_id)
    return redirect('/wishlist')
#################################################################################################
# Wishlist move to Cart btn.
@app.route("/moveToCart/<list_id>/<book_id>")
def moveToCart(list_id, book_id):
    #Find which book it is in the books collection.
    result = db_c.find_one({"_id": ObjectId(book_id)})

    #Insert into the shopping cart collection.
    cart_c.insert_one(result)
    cart_c.update(result, 
    {"$inc": {"quantity": 1}})
    #Remove from displaying in the wishlist.
    if list_id == "1":
        wishlist_c.update_one({"wishlist_id": 1}, {
                          "$pull": {"books_arr": {"_id":ObjectId(book_id)}}})
    elif list_id == "2":
        wishlist_c.update_one({"wishlist_id": 2}, {
                          "$pull": {"books_arr2": {"_id":ObjectId(book_id)}}})
    else:
        wishlist_c.update_one({"wishlist_id": 3}, {
                          "$pull": {"books_arr3": {"_id":ObjectId(book_id)}}})

     

    return redirect('/wishlist')

###################################################################################################
# Wishlist move to cart btn.
@app.route("/createList")
def createList():
    listNum= wishlist_c.count_documents({"user_id":"1"})

    print("NUM OF LISTS: ",listNum)

    if listNum < 3:
        wishlist_c.insert_one({"wishlist":4, "wishlist_title":"Default Title 4","books_arr":[],"user_id":"4"})


    return "" 

###################################################################################################






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
        return render_template("/distinctbooks/" + link + ".html", books=books, authors=authors)
    except Exception as e:
        return dumps({"error": str(e)})



@app.route("/addCart/<book_id>", methods=["GET", "POST"])
def addCart(book_id):
    #result = db.details.find({"book_name": "book_name"})
    result = db_c.find_one(
        {"_id": ObjectId(book_id)}
        
    )
    
    try:
        
        cart_c.insert_one(result)
        cart_c.update(result, 
    {"$inc": {"quantity": 1}})
    except pymongo.errors.DuplicateKeyError:
        pass

    #cart_c.insert_one(result)

    return redirect('/books')

@app.route("/addCartSave/<book_id>", methods=["GET", "POST"])
def addCartSave(book_id):
    
    result = db_c.find_one({"_id": ObjectId(book_id)})

    try:
        cart_c.insert_one(result)
        cart_c.update(result, 
    {"$inc": {"quantity": 1}})
    except pymongo.errors.DuplicateKeyError:
        pass

    save_c.delete_one({"_id": ObjectId(book_id)})

    return redirect('/shoppingcart')

@app.route("/removeCart/<book_id>")
def removeCart(book_id):
    
    cart_c.delete_one({"_id": ObjectId(book_id)})

    return redirect('/shoppingcart')

@app.route("/removeSave/<book_id>")
def removeSave(book_id):
    
    save_c.delete_one({"_id": ObjectId(book_id)})

    return redirect('/shoppingcart')
    
@app.route("/saveLater/<book_id>", methods=["GET", "POST"])
def saveLater(book_id):
    
    result = db_c.find_one({"_id": ObjectId(book_id)})

    try:
        save_c.insert_one(result)
    except pymongo.errors.DuplicateKeyError:
        pass
    
    cart_c.delete_one({"_id": ObjectId(book_id)})

    return redirect('/shoppingcart')

    
@app.route("/shoppingcart")
def shoppingcart():
    cart = cart_c.find()
    save = save_c.find()

    return render_template("/shoppingcart.html", cart = cart, save = save)


app.config['MONGO_DBNAME'] = 'users'
app.config['MONGO_URI'] = 'mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/users'
mongo = PyMongo(app)

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = db_b.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name':request.form['username'], 'password': hashpass})
            session['username'] =  request.form['username']
            return render_template('index.html')

        return 'That username already exists, please go back and create a new one.'

    return render_template('signup.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = db_b.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
            return render_template('index.html')

        return 'Invalid username or password. Please try again'
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/account")
def account():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return redirect(url_for('login'))

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
