# 🎓 Student Record Management System

A simple **Student Record Management System** built using **Python, Streamlit, and MongoDB**. This project demonstrates how to perform basic **CRUD (Create, Read, Update, Delete)** operations using a local MongoDB database.

---

### CRUD 
* C --> Create 
* R --> Retrieve(find)
* U --> Update
* D --> Delete

---

## 🚀 Features

* ➕ Add a new student  (C)
* 📋 View all student records (R)
* 🔍 Search a student by name (R)
* ✏️ Update student details (U)
* ❌ Delete a student record (D)
* 💾 Store data in a local MongoDB database
* 🖥️ Simple and user-friendly Streamlit interface

---

## 🛠️ Tech Stack

* Python
* Streamlit
* MongoDB Community Server (Local)
* PyMongo

---

## 📂 Project Structure

```text
student-record-management/
│
├── app.py              # Streamlit application
├── database.py         # MongoDB connection
├── requirements.txt    # Project dependencies
└── README.md
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/student-record-management.git
cd student-record-management
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start MongoDB

Make sure the MongoDB Community Server is installed and running locally.

Default connection:

```text
mongodb://localhost:27017/
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## 🗄️ Database

**Database Name**

```text
management
```

**Collection Name**

```text
students
```

### Sample Document

```json
{
    "name": "Armaan Gupta",
    "age": 21,
    "course": "B.Tech AI",
    "email": "armaan@example.com",
    "phone": "9876543210"
}
```

---

## 📸 Features Overview

* Add Student
* View Students
* Search Student
* Update Student
* Delete Student

---

## 📚 What I Learned

* Connecting Python with MongoDB using PyMongo
* Performing CRUD operations
* Building interactive web applications using Streamlit
* Managing data with MongoDB collections and documents

---

## 📄 License

This project is created for learning and educational purposes.
