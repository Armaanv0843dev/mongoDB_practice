import streamlit as st
import pandas as pd
from database import collection


# -------------------------
# Sidebar
# -------------------------


page = st.sidebar.radio(
    "Navigation",
    ["Home","Add Records","Show Records","Find Records"]
)


# ==========================================================
# HOME PAGE
# ==========================================================


if page == "Home":

    st.title("📌 MongoDB Record Management System")

    st.markdown("""
    #### Welcome to the MongoDB Record Management System.

    This application demonstrates how to perform basic database operations using MongoDB and Streamlit. It provides a simple and user-friendly interface to manage records efficiently.

    ### 🚀 Features
    - ➕ Add new records to the MongoDB database.
    - 📋 View all stored records in a clean table.
    - ⚡ Fast and interactive web interface powered by Streamlit.
    - 🍃 MongoDB integration for NoSQL data storage.
    ### 🛠️ Technologies Used
    1. Python
    2. Streamlit
    3. MongoDB
    4. PyMongo
    ### 📖 How to Use
    - Navigate to Add Records to insert new data.
    - Open Show Records to view all stored records.
    - All records are saved directly in the connected MongoDB database.
    """)


# ==========================================================
# ADD RECORD PAGE
# ==========================================================


elif page == "Add Records":
    st.title("➕ Add New Record")
    st.write("""
    Use this page to add a new record to the MongoDB database.
    Fill in the details below and click **Submit** to save the information.
    """)

    st.info("""
    📌 Instructions:
    - Enter all required details.
    - Verify the information before submitting.
    - Click **Submit** to store the record.
    """)


    stu_name = st.text_input("Enter your Name.")
    stu_age = st.number_input("Enter your Age.",0,99,1)
    stu_course = st.text_input("Enter your Course.")
    stu_email = st.text_input("Enter your email:",placeholder="example@gmail.com")
    stu_phone = st.number_input("Enter your Phone Number.")


    if st.button("Submit"):
        student = {
            "name" : stu_name,
            "age"  : stu_age,
            "course" : stu_course,
            "email" : stu_email,
            "phone" : stu_phone
        }

        collection.insert_one(student)
        st.success("Inserted Successfully")


# ==========================================================
# VIEW RECORD PAGE
# ==========================================================


elif page == "Show Records":

    st.title("📋 View Records")

    st.write("""
    Browse all records stored in the MongoDB database.
    The table below displays the available data in a clear and organized format.
    """)

    st.info("""
    📌 Features:
    - View all saved records.
    - Refresh the page to load the latest data.
    - Verify stored information easily.
    """)


    # if st.button("Show All Students"):

    students = list(collection.find())

    df = pd.DataFrame(students)

    st.dataframe(df)


# ==========================================================
# VIEW RECORD PAGE
# ==========================================================


else:

    st.title("🔍 Find Records")

    st.write("""
    Search for a specific record stored in the MongoDB database.
    Enter the required details below to quickly locate matching records.
    """)

    st.info("""
    📌 Instructions:
    - Enter the record name in the search field.
    - Click **Search** to find matching records.
    - If a matching record exists, it will be displayed below.
    - If no record is found, an appropriate message will be shown.
    """)

    search_name = st.text_input("Enter the name:",placeholder="Search by name")

    if search_name:
        results = collection.find({
            "name":{
                "$regex" : search_name, # "$regex" → partial match karega
                "$options" : "i"  # "i" --> CASE-insensitive (armaan, Armaan, ARMAAN sab mil jayenge).
            }
        })
    else:
        results = collection.find()

    data = list(results)

    if data:
        df = pd.DataFrame(data)
        df.drop("_id", axis=1, inplace=True)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No matching record found.")

