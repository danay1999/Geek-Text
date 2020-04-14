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
from forms import TitleForm1, TitleForm2, TitleForm3, SignupForm, LoginForm, CreditcardForm, AddressForm, CreditcardForm2, AddressForm2, EditNameForm, EditPasswordForm, EditEmailForm, EditUsernameForm
import os
import json
from flask_login import login_user
from bcrypt import hashpw
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, jsonify, redirect, session, url_for, request,flash



# Database
client = pymongo.MongoClient(
    "mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/test"
)
database = client["book_info"]
db_c = database["details"]
wishlist_c = database['wish_list']  # wishlist collection.
cart_c= database['shopping_cart']
save_c= database['save_for_later']
checkout_c= database['checkout']
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
    if 'email' in session:
        print(session['email'])
        user = session['email']
        form1 = TitleForm1()
        form2 = TitleForm2()
        form3 = TitleForm3()
        if form1.validate_on_submit():
            flash(f'Titles Created Successfully! : {form1.title1.data}','success')
            wishlist_c.update_one({"user_id":user,"wishlist_id":1},{"$set":{"wishlist_title": form1.title1.data}})
            return redirect(url_for('wishlist'))

        if form2.validate_on_submit():
            flash(f'Titles Created Successfully! :  {form2.title2.data}','success')
            wishlist_c.update_one({"user_id":user,"wishlist_id":2},{"$set":{"wishlist_title2": form2.title2.data}})
            return redirect(url_for('wishlist'))

        if form3.validate_on_submit():
            flash(f'Titles Created Successfully! :  {form3.title3.data}','success')
            wishlist_c.update_one({"user_id":user,"wishlist_id":3},{"$set":{"wishlist_title3": form3.title3.data}})
            return redirect(url_for('wishlist'))

        listNum= wishlist_c.count_documents({"user_id": user})

        results = wishlist_c.find({"user_id":user,"wishlist_id":1})
        results2 = wishlist_c.find({"user_id":user,"wishlist_id":2})
        results3 = wishlist_c.find({"user_id":user,"wishlist_id":3})

        if listNum == 1:
        
            return render_template('wishlist.html', results=results, form1=form1, form2=form2,form3=form3)
        elif listNum == 2:
        
            return render_template('wishlist.html', results=results, results2=results2, form1=form1, form2=form2,form3=form3)
        elif listNum == 3:
        
            return render_template('wishlist.html', results=results, results2=results2, results3=results3, form1=form1, form2=form2,form3=form3)

        return render_template('wishlist.html', form1=form1, form2=form2,form3=form3)
    else:
        flash(f'You need to be logged in first!','error')
        return redirect('/login')


###########################################################
@app.route("/add/<list_id>/<book_id>")
def add(list_id,book_id):
    # Add a wishlist item.
    print("ADDED")
    print("LIST NUMBER: ",list_id )
    print("BOOK ID: ",book_id)

    if 'email' in session:
        print(session['email'])
        user = session['email']    

        result = db_c.find_one({"_id": ObjectId(book_id)})

        if list_id == "1":
            wishlist_c.update_one({"user_id":user,"wishlist_id": 1}, {
                            "$addToSet": {"books_arr": result}})
        elif list_id == "2":
            wishlist_c.update_one({"user_id":user,"wishlist_id": 2}, {
                            "$addToSet": {"books_arr2": result}})
        else:
            wishlist_c.update_one({"user_id":user,"wishlist_id": 3}, {
                            "$addToSet": {"books_arr3": result}})
        return redirect('/books')
    return redirect('/login')
###########################################################
@app.route("/remove/<list_id>/<book_id>")
def remove(list_id, book_id):

    if 'email' in session:
        user = session['email']
        if list_id == "1":
            wishlist_c.update_one({"user_id":user,"wishlist_id": 1}, {
                            "$pull": {"books_arr": {"_id": ObjectId(book_id)}}})
        elif list_id == "2":
            wishlist_c.update_one({"user_id":user,"wishlist_id": 2}, {
                            "$pull": {"books_arr2": {"_id": ObjectId(book_id)}}})
        else:
            wishlist_c.update_one({"user_id":user,"wishlist_id": 3}, {
                            "$pull": {"books_arr3": {"_id": ObjectId(book_id)}}})

    return redirect('/wishlist')
######################################################################
# Wishlist move btn
@app.route("/moveBooks/<current>/<list_id>/<book_id>")
def moveBooks(current, list_id, book_id):
    if 'email' in session:
        user = session['email']
        if current == "1":
            if list_id == "2":
                result = db_c.find_one({"_id": ObjectId(book_id)})
                #Add to list 2->
                wishlist_c.update_one({"user_id":user,"wishlist_id": 2}, {
                            "$addToSet": {"books_arr2": result}})
                #Remove from 1st Array of Books
                wishlist_c.update_one({"user_id":user,"wishlist_id": 1}, {
                                "$pull": {"books_arr": {"_id":ObjectId(book_id)}}})
            elif list_id == "3":
                result = db_c.find_one({"_id": ObjectId(book_id)})
                wishlist_c.update_one({"user_id":user,"wishlist_id": 3}, {
                            "$addToSet": {"books_arr3": result}})
                #Remove from 1st Array of Books
                wishlist_c.update_one({"user_id":user,"wishlist_id": 1}, {
                                "$pull": {"books_arr": {"_id":ObjectId(book_id)}}})
        elif current == "2":
            if list_id == "1":
                result = db_c.find_one({"_id": ObjectId(book_id)})
                wishlist_c.update_one({"user_id":user,"wishlist_id": 1}, {
                            "$addToSet": {"books_arr": result}})
                #Remove from 2nd Array of Books
                wishlist_c.update_one({"user_id":user,"wishlist_id": 2}, {
                                "$pull": {"books_arr2": {"_id":ObjectId(book_id)}}})
            elif list_id == "3":
                result = db_c.find_one({"_id": ObjectId(book_id)})
                wishlist_c.update_one({"user_id":user,"wishlist_id": 3}, {
                            "$addToSet": {"books_arr3": result}})
                #Remove from 2nd Array of Books
                wishlist_c.update_one({"user_id":user,"wishlist_id": 2}, {
                                "$pull": {"books_arr2": {"_id":ObjectId(book_id)}}})
        else:
            if list_id == "1":
                result = db_c.find_one({"_id": ObjectId(book_id)})
                wishlist_c.update_one({"user_id":user,"wishlist_id": 1}, {
                            "$addToSet": {"books_arr": result}})
                
                wishlist_c.update_one({"user_id":user,"wishlist_id": 3}, {
                                "$pull": {"books_arr3": {"_id":ObjectId(book_id)}}})
            elif list_id == "2":
                result = db_c.find_one({"_id": ObjectId(book_id)})
                wishlist_c.update_one({"user_id":user,"wishlist_id": 2}, {
                            "$addToSet": {"books_arr2": result}})
                
                wishlist_c.update_one({"user_id":user,"wishlist_id": 3}, {
                                "$pull": {"books_arr3": {"_id":ObjectId(book_id)}}})
        
        return redirect('/wishlist')
    return redirect('/login')
#################################################################################################
@app.route("/moveToCart/<list_id>/<book_id>")
def moveToCart(list_id, book_id):
    #Find which book it is in the books collection.
    if 'email' in session:
        user = session['email']
        result = db_c.find_one({"_id": ObjectId(book_id)})

        #Insert into the shopping cart collection.
        try:
            cart_c.insert_one(result)
            cart_c.update(result, 
        {"$inc": {"quantity": 1}})
            cart_c.update(result,{"$set":{"user_id":user}})
        except pymongo.errors.DuplicateKeyError:
            return redirect('/wishlist')

        return redirect('/wishlist')


###################################################################################################
@app.route("/createList")
def createList():
    if 'email' in session:
        user = session['email']
        listNum= wishlist_c.count_documents({"user_id": user})


        if listNum == 0:
            wishlist_c.insert_one({"wishlist_id":1, "wishlist_title":"Default Title 1","books_arr":[],"user_id":user})
        elif listNum == 1:
            wishlist_c.insert_one({"wishlist_id":2, "wishlist_title2":"Default Title 2","books_arr2":[],"user_id":user})
        elif listNum == 2:
            wishlist_c.insert_one({"wishlist_id":3, "wishlist_title3":"Default Title 3","books_arr3":[],"user_id":user})
        else:
            flash(f'This user already reached their maximum lists!','warning')

        return  redirect('/wishlist')
    return redirect('/login')
###################################################################################################

@app.route("/books", methods=["GET"])
def books():
    try:
        books = db_c.find().sort([("book_name", 1)]) # sort books alphabetically A to Z -Cat
        opt = True

        if 'email' in session:
            user = session['email']
            listNum= wishlist_c.count_documents({"user_id": user})
            if listNum == 0:
                opt = False
                makelist = True
                return render_template("/books.html", books=books,opt=opt, makelist=makelist)
            elif listNum == 1:
                opt = False
                opt1 = True
                return render_template("/books.html", books=books,opt=opt, opt1=opt1)
            elif listNum == 2:
                opt = False
                opt1 = True
                opt2 = True
                return render_template("/books.html", books=books,opt=opt, opt1=opt1 ,opt2=opt2)
            elif listNum == 3:
                opt = False
                opt1 = True
                opt2 = True
                opt3 = True
                return render_template("/books.html", books=books,opt=opt, opt1=opt1 ,opt2=opt2, opt3=opt3)


        return render_template("/books.html",opt=opt, books=books)
    except Exception as e:
        return dumps({"error": str(e)})


@app.route("/sortBooks/<option_id>")
def books_sorting(option_id):
    if option_id=="0":
        books = db_c.find({"topseller": "y"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="1":
        books = db_c.find().sort([("book_name", -1)])
        return render_template('books.html', books=books)
    elif option_id=="2":
        books = db_c.find().sort([("author_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="3":
        books = db_c.find().sort([("publishing_info", 1)])
        return render_template('books.html', books=books)
    elif option_id=="7":
        books = db_c.find({"genre": "Historical Fiction"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="8":
        books = db_c.find({"genre": "Fantasy"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="9":
        books = db_c.find({"genre": "Science Fiction"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="10":
        books = db_c.find({"genre": "Horror"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="11":
        books = db_c.find({"genre": "Crime Fiction"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="12":
        books = db_c.find({"genre": "Political Fiction"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="13":
        books = db_c.find({"genre": "Comedy"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="14":
        books = db_c.find({"genre": "High Fantasy"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="15":
        books = db_c.find({"genre": "Mystery"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="16":
        books = db_c.find({"avg":"5"}).sort([("book_name", 1)])
        return render_template('books.html', books=books)
    elif option_id=="17":
        books = db_c.find({"avg":{'$gte':4}}).sort([("avg",1)])
        return render_template('books.html', books=books)
    elif option_id=="18":
        books = db_c.find({"avg":{'$gte':3}}).sort([("avg",1)])
        return render_template('books.html', books=books)
    elif option_id=="19":
        books = db_c.find({"avg":{'$gte':2}}).sort([("avg",1)])
        return render_template('books.html', books=books)
    elif option_id=="20":
        books = db_c.find({"avg":{'$gte':1}}).sort([("avg",1)])
        return render_template('books.html', books=books)
    elif option_id=="21":
        books = db_c.find().sort([("price",1)])
        return render_template('books.html', books=books)
    elif option_id=="22":
        books = db_c.find().sort([("price",-1)])
        return render_template('books.html', books=books)
    else:
        books = db_c.find().sort([("book_name", 1)])
        return render_template("/books.html", books=books)    


@app.route("/pagination/<items>")
def pagination(items):
    if items=="10":
        books = db_c.find().sort([("book_name", 1)]).limit(10)
        return render_template('books1.html', books=books)
    if items=="20":
        books = db_c.find().sort([("book_name", 1)]).limit(20)
        return render_template('books2.html', books=books)
    else:
        return render_template('books.html', books=books)


@app.route("/pagination/20/1")
def page1_20():
    books = db_c.find().sort([("book_name",1)]).limit(20)
    return render_template('books2.html', books=books)


@app.route("/pagination/20/2")
def page2_20():
    books = db_c.find().sort([("book_name",1)]).skip(20).limit(20)
    return render_template('books2.html', books=books)


@app.route("/pagination/10/1")
def page1_10():
    books = db_c.find().sort([("book_name",1)]).limit(10)
    return render_template('books1.html', books=books)


@app.route("/pagination/10/2")
def page2_10():
    books = db_c.find().sort([("book_name",1)]).skip(10).limit(10)
    return render_template('books1.html', books=books)


@app.route("/pagination/10/3")
def page3_10():
    books = db_c.find().sort([("book_name",1)]).skip(20).limit(10)
    return render_template('books1.html', books=books)
    
           

@app.route("/books/<link>", methods=["GET"])
def distinctbook(link):
    try:
        books = db_b.details.find()
        authors = db_b.author.find()
        comments = db_b.details.find({"link" : link}, {"comment" : ""})
        reviews = db_b.details.find({"link" : link}, {"review" : ""})
        rating = db_b.details.find({"link": link})
        count = 0
        sum = 0
        avg = 0
        for rate in rating: 
            for number in rate['avg_book_rating']:
               count+=1
               sum+=number
        avg=round(sum/count)
        db_b.details.update({"link": link}, {'$set' : {"avg" : avg}})
        opt=True
        if 'email' in session:
            user = session['email']
            listNum= wishlist_c.count_documents({"user_id": user})
            if listNum == 0:
                opt = False
                makelist = True
                return render_template("/distinctbooks/" + link + ".html", books=books,opt=opt, makelist=makelist, comments = comments, authors=authors, avg = avg, reviews=reviews)
            elif listNum == 1:
                opt = False
                opt1 = True
                return render_template("/distinctbooks/" + link + ".html", books=books,opt=opt, opt1=opt1,comments = comments, authors=authors, avg = avg, reviews=reviews)
            elif listNum == 2:
                opt = False
                opt1 = True
                opt2 = True
                return render_template("/distinctbooks/" + link + ".html", books=books,opt=opt, opt1=opt1 ,opt2=opt2,comments = comments, authors=authors, avg = avg, reviews=reviews)
            elif listNum == 3:
                opt = False
                opt1 = True
                opt2 = True
                opt3 = True
                return render_template("/distinctbooks/" + link + ".html", books=books,opt=opt, opt1=opt1 ,opt2=opt2, opt3=opt3, comments = comments, authors=authors, avg = avg, reviews=reviews)
        return render_template("/distinctbooks/" + link + ".html", books=books, comments = comments, authors=authors, avg=avg, opt=opt, reviews=reviews)
    except Exception as e:
        return dumps({"error": str(e)})  


@app.route("/books/<link>/review", methods=['POST', 'GET'])
def message1(link):
    if 'email' in session:
        data = checkout_c.find({"email" : session['email']}).distinct('books')
        print(data)
        

        if link in data:

                if request.method == 'POST' and request.get_json():
                    anonymous = request.form.get('name')
                    print(anonymous)
                    if request.form.get('name'):
                        rates = request.get_json(force=True)
                        email = session['email']
                        cursor = db_b.account.find_one({"email": email})
                        rate = json.dumps(rates)
                        db_b.details.update({"link": link}, {'$push': {"avg_book_rating": rates }})
                        db_b.details.update({"link": link}, {'$push': {"review": "Anonymous : Rate Given :" + rate }})
                        res = make_response(jsonify({"message": "OK"}), 200)
                        return res
                    else:
                        rates = request.get_json(force=True)
                        email = session['email']
                        cursor = db_b.account.find_one({"email": email})
                        rate = json.dumps(rates)
                        db_b.details.update({"link": link}, {'$push': {"avg_book_rating": rates }})
                        db_b.details.update({"link": link}, {'$push': {"review": cursor['name'] + " : Rate Given :" + rate }})
                        res = make_response(jsonify({"message": "OK"}), 200)
                        return res

    
                if request.method == 'POST' and request.form['comment']:
                    comment = request.form['comment']
                    if 'name' not in request.form:
                        email = session['email']
                        cursor = db_b.account.find_one({"email": email})
                        comments = db_b.details.update({"link": link}, {'$push': {"comment": cursor['name'] + " : " + request.form.get('comment')}})
                        return redirect("/books/"+link+"/review")
                    else:
                        if "Anonymous" in request.form['name']:
                            email = session['email']
                            cursor = db_b.account.find_one({"email": email})
                            comments = db_b.details.update({"link": link}, {'$push': {"comment": "Anonymous" + " : " + request.form.get('comment')}})
                            return redirect("/books/"+link+"/review")
                        else:
                            email = session['email']
                            cursor = db_b.account.find_one({"email": email})
                            comments = db_b.details.update({"link": link}, {'$push': {"comment": cursor['username'] + " : " + request.form.get('comment')}})
                            return redirect("/books/"+link+"/review")
                else:
                    return render_template('/bookreviews/' + link +'review.html')
        else:
                flash(f'You need to buy this book in order to review it!','success')
                return redirect(url_for('distinctbook', link = link))
    flash(f'You need to Sign In to review this book!','success')
    return redirect(url_for('login'))

@app.route("/addCart/<book_id>", methods=["GET", "POST"])
def addCart(book_id):
    #result = db.details.find({"book_name": "book_name"})
    result = db_c.find_one(
        {"_id": ObjectId(book_id)}
        
    )
    
    try:
        if 'email' in session:
            cart_c.insert_one(result)
            cart_c.update(result, 
    {"$inc": {"quantity": 1}})
        else:
            flash(f'You need to sign in to add a book to your cart!','success')
            return redirect(url_for('login'))
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

@app.route("/shoppingcart", methods=["GET", "POST"])
def shoppingcart():
    if 'email' in session :

        cart = cart_c.find()
        save = save_c.find()

        if request.method == 'POST' and request.get_json():
                
                list = []
                quantity = request.get_json('test')
                link = request.get_json('test')
                link2 = list.append(quantity)
                
                for something in list:
                    print(something['link2'])
                    print(something['quantity'])
               
                
                cart_c.update({"link": something['link2']}, {'$set': {"quantity": something['quantity']}})
                res = make_response(jsonify({"message": "OK"}), 200)

    else:
        flash(f'You need to sign in to view your cart!','success')
        return redirect(url_for('login'))


    return render_template("/shoppingcart.html", cart = cart, save = save)

@app.route("/checkout")
def checkout():
    if 'email' in session:
        checkout_c.insert({"email": session['email']})
        data = cart_c.find().distinct('link')
        for data in data:
            print(data)
            checkout_c.update({"email": session['email']}, {'$addToSet': {"books": data}}, upsert=True)
    
    
    flash(f'You have purchased the books!','success')
    return redirect('/shoppingcart')

app.config['MONGO_DBNAME'] = 'book_info'
app.config['MONGO_URI'] = 'mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/book_info'
mongo = PyMongo(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        account = mongo.db.account
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            user = users.insert_one({'name': form.name.data, 'username': form.username.data, 'email': form.email.data,
                    'password': hashed_password})
            account.insert_one({'name': form.name.data, 'username': form.username.data, 'email': form.email.data,
                    'password': hashed_password})
            session['email'] =  request.form['email']
            flash(f"Thank you for signing up", 'success')
            return redirect(url_for('account'))
        flash(f"User already exists with this email, please Log In.", 'success')
    return render_template('signup.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate(): 
        users = mongo.db.account
        login_user = users.find_one({'email' : request.form['email']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['email'] =  request.form['email']
                return redirect(url_for('account')) 
        flash(f"Invalid email/password combination", 'error')  
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')

@app.route("/account", methods=['GET'])
def account():
    form = LoginForm(request.form)
    if 'email' in session:
        users = mongo.db.account
        cards = mongo.db.account
        #address = mongo.db.address
        #email = users.find_one({"email" : form.email.data})
        email = session['email']
        print(email)        
        
        printemail = users.find_one({"email": session['email']})
        
        return render_template('account.html', printemail=printemail)
    return redirect(url_for('login'))


@app.route("/editname", methods=['POST', 'GET'])
def editname():
    form = EditNameForm(request.form)
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        account = mongo.db.account

        user = users.insert_one({'name': form.name.data})
        account.update({"email": session['email']}, {'$set': {'name': form.name.data}},upsert= True)
        flash(f"Information has been updated", 'success')
        return redirect(url_for('account'))
    return render_template('editname.html', form=form)


@app.route("/editusername", methods=['POST', 'GET'])
def editusername():
    form = EditUsernameForm(request.form)
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        account = mongo.db.account

        user = users.find_one({'username': form.username.data})
        account.update({"email": session['email']}, {'$set': {'username': form.username.data}},upsert= True)
        flash(f"Information has been updated", 'success')
        return redirect(url_for('account'))
    return render_template('editusername.html', form=form)
   
@app.route("/editpassword", methods=['POST', 'GET'])
def editpassword():
    form = EditPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        account = mongo.db.account

        hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        user = users.insert_one({'password': hashed_password})
        account.update({"email": session['email']}, {'$set': {'password': hashed_password}},upsert= True)
        flash(f"Information has been updated", 'success')
        return redirect(url_for('account'))
    return render_template('editpassword.html', form=form)

@app.route("/editemail", methods=['POST', 'GET'])
def editemail():
    form = EditEmailForm(request.form)
    if request.method == 'POST' and form.validate():
        users = mongo.db.users
        account = mongo.db.account


        user = users.insert_one({'email': form.email.data})
        account.update({"email": session['email']}, {'$set': {'email': form.email.data}},upsert= True)
        session['email'] =  request.form['email']
        flash(f"Information has been updated", 'success')
        return redirect(url_for('account'))
    return render_template('editemail.html', form=form)

@app.route("/editsignup", methods=['POST', 'GET'])
def editsignup():
    users = mongo.db.users
    account = mongo.db.account
    email = session['email']
    print(email)        
        
    printemail = account.find_one({"email": session['email']})

    return render_template('editsignup.html', printemail=printemail)

   

@app.route("/cards", methods=['POST', 'GET'])
def cards():
    form = CreditcardForm(request.form)
    if request.method == 'POST' and form.validate():
        cards = mongo.db.cards
        cards_id = cards.insert_one({'card_nickname': form.card_nickname.data,'card_type': form.card_type.data, 'name_on_card': form.name_on_card.data, 'card_number': form.card_number.data, 'cvv': form.cvv.data,'exp_month': form.exp_month.data, 'exp_year': form.exp_year.data})
        account = mongo.db.account
        account.update({"email": session['email']}, {'$set': {'card_nickname': form.card_nickname.data,'card_type': form.card_type.data,'name_on_card': form.name_on_card.data, 'card_number': form.card_number.data, 'cvv': form.cvv.data,'exp_month': form.exp_month.data, 'exp_year': form.exp_year.data}}, upsert= True)
        return redirect(url_for('account')) 
    return render_template('cards.html', form=form)

@app.route("/address", methods=['POST', 'GET'])
def address():
    form = AddressForm(request.form)
    if request.method == 'POST':
        address = mongo.db.address
        address.insert({'nickname': form.nickname.data, 'name': form.name.data, 'address_line_1': form.address_line_1.data, 'address_line_2': form.address_line_2.data, 'city': form.city.data, 'state' : form.state.data, 'zip' : form.zip.data})
        account = mongo.db.account
        account = mongo.db.account
        account.update({"email": session['email']}, {'$set': {'nickname': form.nickname.data, 'name': form.name.data, 'address_line_1': form.address_line_1.data, 'address_line_2': form.address_line_2.data, 'city': form.city.data, 'state' : form.state.data, 'zip' : form.zip.data}}, upsert= True)
        return redirect(url_for('account'))
    return render_template('address.html')

@app.route("/address2", methods=['POST', 'GET'])
def address2():
    form = AddressForm2(request.form)
    if request.method == 'POST':
        address = mongo.db.address
        address.insert({'nickname2': form.nickname2.data, 'name2': form.name2.data, 'address_line_1_2': form.address_line_1_2.data, 'address_line_2_2': form.address_line_2_2.data, 'city2': form.city2.data, 'state2' : form.state2.data, 'zip2' : form.zip2.data})
        account = mongo.db.account
        account = mongo.db.account
        account.update({"email": session['email']}, {'$set': {'nickname2': form.nickname2.data, 'name2': form.name2.data, 'address_line_1_2': form.address_line_1_2.data, 'address_line_2_2': form.address_line_2_2.data, 'city2': form.city2.data, 'state2' : form.state2.data, 'zip2' : form.zip2.data}}, upsert= True)
        return redirect(url_for('account'))
    return render_template('address2.html')

@app.route("/cards2", methods=['POST', 'GET'])
def cards2():
    form = CreditcardForm2(request.form)
    if request.method == 'POST' and form.validate():
        cards = mongo.db.cards
        cards_id = cards.insert_one({'card_nickname2': form.card_nickname2.data, 'card_type2': form.card_type2.data,'name_on_card2': form.name_on_card2.data, 'card_number2': form.card_number2.data, 'cvv2': form.cvv2.data,'exp_month2': form.exp_month2.data, 'exp_year2': form.exp_year2.data})
        account = mongo.db.account
        account.update({"email": session['email']}, {'$set': {'card_nickname2': form.card_nickname2.data,'card_type2': form.card_type2.data, 'name_on_card2': form.name_on_card2.data, 'card_number2': form.card_number2.data, 'cvv2': form.cvv2.data,'exp_month2': form.exp_month2.data, 'exp_year2': form.exp_year2.data}}, upsert= True)
        return redirect(url_for('account')) 
    return render_template('cards2.html', form=form)



@app.route("/profile", methods=['GET'])
def profile():
    if 'email' in session:
        users = mongo.db.users
        cards = mongo.db.cards
        address = mongo.db.address

        printuser = users.find_one({"email": "osito@gmail.com"}, {"email": ""})
        printcard = cards.find_one({"name_on_card" : "Patricia Toledo"}, {"card_number": ""})
        #printaddress = address.find_one({"_id": ObjectId(addresss_id)})
        print(printuser)
        #print(printaddress)
        print(printcards)
        return redirect(url_for('login'))
    return render_template('account.html', printuser=printuser, printcard=printcard)
#, printaddress=printaddress {{profile.printaddress}}





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
