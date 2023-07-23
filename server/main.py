from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())

printer = pprint.PrettyPrinter()

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://amanleyskj:{password}@yiipcluster.of7olmw.mongodb.net/"

client = MongoClient(connection_string)

# dbs = client.list_database_names()
# print(dbs)

db = client.yiip
collections = db.list_collection_names()

def register_user():
    # define collection we are accessing here
    collection = db.users
    # this is a test; for a real function, we'll be tying in data from the frontend
    data = {
        # TEST: below values will be coming from the frontend user form
        "first_name" : "Miho",
        "last_name" : "Irie",
        "email" : "japan@tochigi.com" ,
        "password" : "1ABd22C2afgd3" ,
        "birthday" : "12512173321" 
    }
    # insert_one is a built-in function of collection saccess
    collection.insert_one(data)
    # gives us the ID of what was just inserted into the collection
    inserted_id = collection.insert_one(data).inserted_id
    print(f"The id of {inserted_id} has been created and should now reflect in the database.")

# this ID is known as a BSON object ID; it's a specific type, and not just an integer
# register_user()

# if you make a db that doesn't exist, MongoDB will create it
production = client.production
person_collection = production.person_collection

yiip = client.yiip
user_collection = yiip.users


# *****
# CREATING DOCUMENTS
# def create_documents():
#     first_names = ["Jack", "Jill", "Billy", "Bob"]
#     last_names = ["Smith", "Parker", "Relationne", "Pevpy"]

#     ages = [25, 25, 28, 50]

#     docs = []

#     for first_name, last_name, age in zip(first_names, last_names, ages):
#         document = {"first_name" : first_name, "last_name" : last_name, "age" : age}
#         docs.append(document)

#     person_collection.insert_many(docs)

#         # below is one option; you can also do a insert_many method
#         # person_collection.insert_one(document)
# create_documents()


# *****
# READING DOCUMENTS

def find_all_users():
    users = user_collection.find()

    for user in users:
        printer.pprint(user)

# below should be adjusted for user input; the Anthony part should be a user input
def find_user_by_name():
    user = user_collection.find_one({"first_name" : "BILLY"})
    if user == None:
        print("Nothing was returned!")
    else:
        printer.pprint(user)

def total_users():
    count = user_collection.count_documents(filter = {})
    print("Number of users is", count)

# total_users()

def get_user_by_id(user_id):
    # below import can be put somewhere else; this just makes it self-contained
    from bson.objectid import ObjectId

    # we need to convert to the following because they need to be this special object; the strings we have as IDs aren't going to work here
    _id = ObjectId(user_id)

    user = user_collection.find_one({"_id" : _id})
    printer.pprint(user)

# get_user_by_id("64bc8c1fce74502b2ab2bfcc")

def get_age_range(min_age, max_age):
    query = {"$and" : [
            {"age" : {"$gte" : min_age}},
            {"age" : {"$lte" : max_age}}
            ]}
    
    users = user_collection.find(query).sort("age")
    for user in users:
        printer.pprint(user)

get_age_range()