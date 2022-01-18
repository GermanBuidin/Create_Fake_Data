from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://German:Password2811@cluster0.skc3a.mongodb.net/testdata?retryWrites=true&w=majority")
db = cluster["testdata"]
collection = db["testcollection"]
