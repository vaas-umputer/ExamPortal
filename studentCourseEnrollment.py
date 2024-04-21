#import pandas and numpy and streanmlit
import pandas as pd
import numpy as np
import streamlit as st
import mysql.connector


#create a fucntion to create student course enrollment
#get a csv file that has the student register number and course code
#columns number are not known; what is known is there are register numbers and each register number will have a number of courses enrolled in , each course will have a course code annd course name and each column corressponsing to a studetn reguster number is a course he is enrolled in
#there is a mysql table names 'course_stud' with columns - coursecode and studentregisternumber
#based on the values in the csv file, records needs to be inserted into the table; say student 1 enrolls in 2 subjects; there has to be 2 records inserted for him

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cip"
    )

def studentCourseEnrollment():
    st.title("Student Course Enrollment")
    st.write("This application is used to enroll students in courses")
    st.write("Please upload the csv file that has the student register number and course code")
    file = st.file_uploader("Upload file", type = ['csv'])
    if file is not None:
        df = pd.read_csv(file)
        st.write(df)
        if st.button("Create Enrollment"):
            try:
                db = connect_to_database()
                cursor = db.cursor()
                for index, row in df.iterrows():
                    student_register_number = row[0]
                    for i in range(1, len(row)):
                        course_code = row[i]
                        if not check_duplicate_entry(course_code, student_register_number):
                            cursor.execute("INSERT INTO coursestudents (courseCode, studentRegNum) VALUES (%s, %s)", (course_code, student_register_number))
                            db.commit()
                            #query = "insert into course_stud values('"+course_code+"','"+student_register_number+"')"
                            #st.write(query)
                            #st.write("Record inserted successfully")
                        else:
                            st.error(f"Student with register number {student_register_number} is already enrolled in the course {course_code}")
                            break
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
            
    else:
        st.write("Please upload the file")
#insert a duplicate entry check function for the student course enrollment
#check if the student is already enrolled in the course
#this function happens before the record is inserted into the table
#if it returns true, the record is not inserted
def check_duplicate_entry(course_code, student_register_number):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM coursestudents WHERE courseCode = %s AND studentRegNum = %s", (course_code, student_register_number))
    student = cursor.fetchone()
    if student:
        return True
    else:
        return False



studentCourseEnrollment()

