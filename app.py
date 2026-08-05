import streamlit as st
from database import collection

st.title("Simple Record Management")

st.markdown("""
Welcome , this app is for learning the basics of MongoDB and how data flow from User to Database as User input data to given form.
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

