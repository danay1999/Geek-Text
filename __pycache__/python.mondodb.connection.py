from pymongo import MongoClient
from bson import ObjectId
import pymongo

client = MongoClient("mongodb+srv://bdiaz071:0312651pw@bookstore-2edyi.mongodb.net/test")
database = client["test"]
db_c = database["clients"]
print("Database connected...")

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
