import streamlit as st

import mysql.connector
import login

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="examportal"
    )

def register_user():
    user_type = st.selectbox("Select user type", ["Student", "Professor"])
    if user_type == "Student":
        register_student()
    elif user_type == "Professor":
        register_professor()

def register_student():
    register_number = st.text_input("Enter register number")
    name = st.text_input("Enter name")
    department = st.text_input("Enter department")
    email = st.text_input("Enter email")
    pno = st.text_input("Enter phone number")
    username = register_number
    password = register_number
    if st.button("Register"):
        save_user(username, password, name, department, email, "student", pno)

def register_professor():
    professor_id = st.text_input("Enter professor id")
    name = st.text_input("Enter name")
    department = st.text_input("Enter department")
    email = st.text_input("Enter email")
    professor_position = st.selectbox("Select professor position", ["Professor", "Assistant Professor", "Associate Professor", "Teaching Fellow"])
    pno = st.text_input("Enter phone number")
    username = professor_id
    password = professor_id
    if st.button("Register"):
        save_user_p(username, password, name, department, email, "professor", professor_position, pno)

def save_user(username, password, name, department, email, user_type, pno):
    connection = connect_to_database()
    cursor = connection.cursor()
    query1 = "INSERT INTO user (userName, password, phoneNum, userRole) VALUES (%s, %s, %s, %s)"
    values = (username, password, pno, user_type)
    query2 = "INSERT INTO student (registerNumber, studentName, studentDepartment, studentEmail) VALUES (%s, %s, %s, %s)"
    values1 = (username, name, department, email)
    cursor.execute(query1, values)
    cursor.execute(query2, values1)
    connection.commit()
    st.success("User registered successfully!")

def save_user_p(username, password, name, department, email, user_type, pos, pno):
    connection = connect_to_database()
    cursor = connection.cursor()
    query1 = "INSERT INTO user (userName, password, phoneNum, userRole) VALUES (%s, %s, %s, %s)"
    values = (username, password, pno, user_type)
    query2 = "INSERT INTO professor (professorID, professorName, professorPosition, professorDepartment, professorEmail) VALUES (%s, %s, %s, %s,%s)"
    values1 = (username, name, pos, department, email)
    cursor.execute(query1, values)
    cursor.execute(query2, values1)
    connection.commit()
    st.success("User registered successfully!")

st.title("Registration Page")
st.write("Please enter the user details")
register_user()
#add a link to the login page
st.write("Already have an account? [Login here](login.login())")