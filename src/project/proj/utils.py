from bson import ObjectId
from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017/compressors=disabled&gssapiServiceName=mongodb")

db = client.testdata
collection = db["collection"]

#print(list(collection.find({"_id": ObjectId('61fa75dcf28e1abae6acb8cd')}, {"_id":False})))
print(dir(collection))
