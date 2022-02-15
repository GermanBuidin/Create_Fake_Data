from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/compressors=disabled&gssapiServiceName=mongodb")
db = client.testdata
collection = db["schemas"]



