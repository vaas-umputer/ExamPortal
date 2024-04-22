#add a loin page here

import streamlit as st

import mysql.connector


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="examportal"
    )

def login():
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE userName = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result:
            st.success("Login successful!")
            if result[3] == "student":
                st.write("Welcome student!")
            elif result[3] == "professor":
                st.write("Welcome professor!")
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    login()
