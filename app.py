"""
app.py
------
Main Streamlit application for the Student Record Management System.
Handles all UI pages: Home, Add, Show, Find, Update, Delete.
"""

import re
import streamlit as st
import pandas as pd
from database import (
    insert_record,
    find_all_records,
    find_records_by_name,
    update_record,
    delete_record,
)


# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Student Record Management",
    page_icon="🎓",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Add Records", "Show Records", "Find Records", "Update Records", "Delete Records"],
)


# ===========================================================================
# HOME PAGE
# ===========================================================================

if page == "Home":

    st.title("📌 MongoDB Record Management System")

    st.write("### Why MongoDB?")

    st.markdown("""
    - I learned MongoDB to understand how modern applications store and manage
      data using a flexible NoSQL database. I wanted to gain practical experience
      with CRUD operations, database design, searching, updating, and deleting records.

    - I also used MongoDB in a Record Management System built with Python and
      Streamlit, which helped me understand how a database connects with a
      real-world application.
    """)

    st.markdown("""
    #### Welcome to the MongoDB Record Management System.

    This application demonstrates how to perform basic database operations using
    MongoDB and Streamlit. It provides a simple and user-friendly interface to
    manage records efficiently.

    ### 🚀 Features
    - ➕ Add new records to the MongoDB database.
    - 📋 View all stored records in a clean table.
    - 🔍 Search records by name (case-insensitive, partial match).
    - ✏️ Update existing records in-place.
    - 🗑️ Delete records permanently.
    - ⚡ Fast and interactive web interface powered by Streamlit.
    - 🍃 MongoDB integration for NoSQL data storage.

    ### 🛠️ Technologies Used
    1. Python
    2. Streamlit
    3. MongoDB
    4. PyMongo

    ### 📖 How to Use
    - Navigate to **Add Records** to insert new data.
    - Open **Show Records** to view all stored records.
    - Use **Find Records** to search by name.
    - Use **Update Records** to modify existing data.
    - Use **Delete Records** to permanently remove a record.
    """)


# ===========================================================================
# ADD RECORD PAGE
# ===========================================================================

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

    stu_name   = st.text_input("Name", placeholder="e.g. Armaan Gupta")
    stu_age    = st.number_input("Age", min_value=1, max_value=99, value=18)
    stu_course = st.text_input("Course", placeholder="e.g. B.Tech AI")
    stu_email  = st.text_input("Email", placeholder="example@gmail.com")
    # Phone stored as string to preserve leading zeros and avoid float issues
    stu_phone  = st.text_input("Phone Number", placeholder="e.g. 9876543210")

    if st.button("Submit"):
        # --- Input validation ---
        errors = []
        if not stu_name.strip():
            errors.append("Name cannot be empty.")
        if not stu_course.strip():
            errors.append("Course cannot be empty.")
        if not stu_email.strip():
            errors.append("Email cannot be empty.")
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", stu_email):
            errors.append("Please enter a valid email address.")
        if not stu_phone.strip():
            errors.append("Phone number cannot be empty.")
        elif not stu_phone.strip().lstrip("+").isdigit():
            errors.append("Phone number must contain only digits (optionally starting with +).")

        if errors:
            for err in errors:
                st.error(err)
        else:
            try:
                insert_record(
                    name=stu_name.strip(),
                    age=int(stu_age),
                    course=stu_course.strip(),
                    email=stu_email.strip(),
                    phone=stu_phone.strip(),
                )
                st.success("✅ Record inserted successfully!")
            except Exception as e:
                st.error(f"Database error: {e}")


# ===========================================================================
# SHOW RECORDS PAGE
# ===========================================================================

elif page == "Show Records":

    st.title("📋 View Records")

    st.write("""
    Browse all records stored in the MongoDB database.
    The table below displays up to 100 records in a clear and organized format.
    """)

    st.info("""
    📌 Features:
    - View all saved records.
    - Refresh the page to load the latest data.
    - Verify stored information easily.
    """)

    students = find_all_records(limit=100)

    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True)
        st.caption(f"Showing {len(students)} record(s). Maximum display limit: 100.")
    else:
        st.warning("No records found in the database.")


# ===========================================================================
# FIND RECORDS PAGE
# ===========================================================================

elif page == "Find Records":

    st.title("🔍 Find Records")

    st.write("""
    Search for a specific record stored in the MongoDB database.
    Enter a name below to quickly locate matching records.
    """)

    st.info("""
    📌 Instructions:
    - Enter the record name in the search field.
    - Results update automatically as you type.
    - If no record is found, an appropriate message will be shown.
    """)

    search_name = st.text_input("Search by name", placeholder="Start typing a name…")

    if search_name.strip():
        data = find_records_by_name(search_name.strip())
    else:
        data = find_all_records()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No matching record found.")


# ===========================================================================
# UPDATE RECORD PAGE
# ===========================================================================

elif page == "Update Records":

    st.title("✏️ Update Record")

    st.write("""
    Update an existing record stored in the MongoDB database.
    Search for a record by name, modify the required fields, and save the changes.
    """)

    st.info("""
    📌 Instructions:
    - Enter the record exact name to search.
    - Modify the required information.
    - Click **Update** to save changes.
    """)

    search_name = st.text_input("Enter Name to Search")

    if st.button("Search"):
        from database import collection  # direct access only for find_one here
        record = collection.find_one({"name": search_name})
        if record:
            st.session_state.record = record
            st.success("Record found ✅")
        else:
            st.session_state.record = None
            st.error("Record not found ❌")

    if st.session_state.get("record"):
        record = st.session_state.record

        new_name   = st.text_input("Name",         value=record["name"])
        new_age    = st.number_input("Age",         min_value=0, max_value=100, value=int(record["age"]))
        new_course = st.text_input("Course",        value=record["course"])
        new_email  = st.text_input("Email",         value=record["email"])
        new_phone  = st.text_input("Phone Number",  value=str(record["phone"]))

        if st.button("Update"):
            update_record(
                old_name=search_name,
                new_name=new_name.strip(),
                new_age=int(new_age),
                new_course=new_course.strip(),
                new_email=new_email.strip(),
                new_phone=new_phone.strip(),
            )
            st.success("🎉 Record updated successfully!")

            # Refresh session state with updated values
            st.session_state.record = {
                "name":   new_name,
                "age":    new_age,
                "course": new_course,
                "email":  new_email,
                "phone":  new_phone,
            }


# ===========================================================================
# DELETE RECORD PAGE
# ===========================================================================

elif page == "Delete Records":

    st.title("🗑️ Delete Record")

    st.write("""
    Delete an existing record from the MongoDB database.
    Search for a record by name and permanently remove it.
    """)

    st.warning("⚠️ Warning: Deleted records cannot be recovered.")

    search_name = st.text_input("Enter Full Name to Search and Delete")

    if st.button("Search"):
        from database import collection  # direct access only for find_one here
        record = collection.find_one({"name": search_name})
        if record:
            st.session_state.delete_record = record
            st.success("Record found ✅")
        else:
            st.session_state.delete_record = None
            st.error("Record not found.")

    if st.session_state.get("delete_record"):
        record = st.session_state.delete_record

        st.write("### Record Details")
        st.write(f"**Name:** {record['name']}")
        st.write(f"**Age:** {record['age']}")
        st.write(f"**Course:** {record['course']}")
        st.write(f"**Email:** {record['email']}")
        st.write(f"**Phone:** {record['phone']}")

        # Delete button is inside this block — it is only shown when a record has been found
        if st.button("Delete", type="primary"):
            deleted = delete_record(search_name)
            if deleted:
                st.success("✅ Record deleted successfully!")
                st.session_state.delete_record = None  # clear state after deletion
            else:
                st.error("❌ Record not found.")


