from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["management"]

collection = db["student"]


def update_record(old_name, new_name, new_age, new_course, new_email, new_phone):
    collection.update_one(
        {"name": old_name},      # Jis record ko update karna hai
        {
            "$set": {
                "name": new_name,
                "age": new_age,
                "course": new_course,
                "email": new_email,
                "phone": new_phone
            }
        }
    )