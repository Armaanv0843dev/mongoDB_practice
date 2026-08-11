"""
database.py
-----------
MongoDB connection and CRUD helper functions for the Student Record
Management System.

The MongoClient is wrapped in @st.cache_resource so that only ONE connection
is created for the lifetime of the Streamlit server process, regardless of
how many times the app reruns.
"""

import streamlit as st
from pymongo import MongoClient


# ---------------------------------------------------------------------------
# Connection (cached — created only once per server lifetime)
# ---------------------------------------------------------------------------

@st.cache_resource
def _get_collection():
    """Return the cached MongoDB collection object."""
    client = MongoClient(st.secrets["mongo"]["uri"])
    db = client["management"]
    return db["student"]


collection = _get_collection()


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------

def insert_record(name: str, age: int, course: str, email: str, phone: str) -> None:
    """Insert a new student document into the collection."""
    student = {
        "name": name,
        "age": age,
        "course": course,
        "email": email,
        "phone": phone,
    }
    collection.insert_one(student)


def find_all_records(limit: int = 100) -> list:
    """Return up to *limit* student documents (without _id)."""
    return list(
        collection.find({}, {"_id": 0}).limit(limit)
    )


def find_records_by_name(search_name: str) -> list:
    """Return documents whose name contains *search_name* (case-insensitive)."""
    query = {
        "name": {
            "$regex": search_name,
            "$options": "i",   # case-insensitive match
        }
    }
    return list(collection.find(query, {"_id": 0}))


def update_record(
    old_name: str,
    new_name: str,
    new_age: int,
    new_course: str,
    new_email: str,
    new_phone: str,
) -> None:
    """Update the first document whose name matches *old_name*."""
    collection.update_one(
        {"name": old_name},
        {
            "$set": {
                "name": new_name,
                "age": new_age,
                "course": new_course,
                "email": new_email,
                "phone": new_phone,
            }
        },
    )


def delete_record(name: str) -> int:
    """
    Delete the first document whose name matches *name*.

    Returns the number of deleted documents (0 or 1).
    """
    result = collection.delete_one({"name": name})
    return result.deleted_count