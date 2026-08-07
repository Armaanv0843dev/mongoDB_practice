import streamlit as st
import pandas as pd
from database import collection
from database import update_record
from database import delete_record


# -------------------------
# Sidebar
# -------------------------


page = st.sidebar.radio(
    "Navigation",
    ["Home","Add Records","Show Records","Find Records","Update Records","Delete Records"]
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


elif page == "Find Records":

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


# ==========================================================
# UPDATE PAGE
# ==========================================================


elif page == "Update Records":

    st.title("✏️ Update Record")

    st.write("""
    Update an existing record stored in the MongoDB database.
    Search for a record, modify the required fields, and save the changes.
    """)

    st.info("""
    📌 Instructions:
    - Enter the record name to search.
    - Modify the required information.
    - Click **Update** to save changes.
    """)

    search_name = st.text_input("Enter Name to Update")

    # Search Button
    if st.button("Search"):

        record = collection.find_one({"name": search_name})

        if record:
            st.session_state.record = record
            st.success("Record Found ✅")
        else:
            st.session_state.record = None
            st.error("Record Not Found ❌")

    # Agar record mil gaya ho
    if "record" in st.session_state and st.session_state.record:

        record = st.session_state.record

        new_name = st.text_input(
            "Name",
            value=record["name"]
        )

        new_age = st.number_input(
            "Age",
            min_value=0,
            max_value=100,
            value=record["age"]
        )

        new_course = st.text_input(
            "Course",
            value=record["course"]
        )

        new_email = st.text_input(
            "Email",
            value=record["email"]
        )

        new_phone = st.number_input(
            "Phone Number",
            value=int(record["phone"])
        )

        if st.button("Update"):

            update_record(
                search_name,
                new_name,
                new_age,
                new_course,
                new_email,
                new_phone
            )

            st.success("🎉 Record Updated Successfully!")

            # Updated data dikhane ke liye
            st.session_state.record = {
                "name": new_name,
                "age": new_age,
                "course": new_course,
                "email": new_email,
                "phone": new_phone
            }


# ==========================================================
# DELETE PAGE
# ==========================================================

else: 

    st.title("🗑️ Delete Record")

    st.write("""
    Delete an existing record from the MongoDB database.
    Search for a record by name and permanently remove it.
    """)

    st.warning("""
    ⚠️ Warning:
    Deleted records cannot be recovered.
    """)

    search_name = st.text_input("Enter Name to Search and Delete")

    if st.button("Search"):

        record = collection.find_one({"name": search_name})

        if record:
            st.session_state.delete_record = record
        else:
            st.session_state.delete_record = None
            st.error("Record Not Found")

    if "delete_record" in st.session_state and st.session_state.delete_record:

        record = st.session_state.delete_record

        st.write("### Record Details")

        st.write(f"**Name:** {record['name']}")
        st.write(f"**Age:** {record['age']}")
        st.write(f"**Course:** {record['course']}")
        st.write(f"**Email:** {record['email']}")
        st.write(f"**Phone:** {record['phone']}")

    if st.button("Delete"):

        deleted = delete_record(search_name)

        if deleted:
            st.success("✅ Record Deleted Successfully!")
        else:
            st.error("❌ Record Not Found.")