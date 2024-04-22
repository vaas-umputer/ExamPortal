import pandas as pd
import numpy as np
import streamlit as st
import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="examportal"
    )

#add an option to delete student course enrollment
#this will be based on the student register number and course code
#the user will input the student register number and course code
#the record will be deleted from the table
def delete_course_enrollment():
    st.title("Delete Student Course Enrollment")
    #student_register_number = st.text_input("Enter the student register number")
    course_code = st.text_input("Enter the course code")
    if st.button("Delete Enrollment"):
        try:
            db = connect_to_database()
            cursor = db.cursor()
            cursor.execute("Delete from courselist where courseCode=%s", (course_code))
            cursor.execute("Delete from coursestudents where courseCode=%s", (course_code))
            db.commit()
            st.write("Records deleted successfully")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")


delete_course_enrollment()