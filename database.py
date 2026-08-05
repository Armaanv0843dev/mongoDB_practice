from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["management"]

collection = db["student"]