import streamlit as st
import mysql.connector

# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cip"
    )

# Create table if not exists
def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INT AUTO_INCREMENT PRIMARY KEY,
            register_number VARCHAR(50) UNIQUE,
            password VARCHAR(100)
        )
    """)
    cursor.execute("COMMIT")

# Admin page to add students
def admin_page():
    st.title("Admin Page - Add Student")
    register_number = st.text_input("Enter Register Number:")
    password = st.text_input("Enter Password:", type="password")
    if st.button("Add Student"):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO students (register_number, password) VALUES (%s, %s)", (register_number, password))
            db.commit()
            st.success("Student added successfully!")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

# Student page to login
def student_page():
    st.title("Student Page - Login")
    register_number = st.text_input("Enter Register Number:")
    password = st.text_input("Enter Password:", type="password")
    if st.button("Login"):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students WHERE register_number = %s AND password = %s", (register_number, password))
        student = cursor.fetchone()
        if student:
            st.success("Successfully logged in!")
        else:
            st.error("Invalid credentials")

# Main function
def main():
    st.sidebar.title("Portal Selection")
    page = st.sidebar.radio("Go to", ["Admin Page", "Student Page"])
    if page == "Admin Page":
        admin_page()
    elif page == "Student Page":
        student_page()

if __name__ == "__main__":
    db = connect_to_database()
    create_table(db.cursor())
    main()
