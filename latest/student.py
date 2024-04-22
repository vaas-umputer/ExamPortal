#replicate the layout of professor.py in student.py
#add a side panel on left and have options
#options: take exam, view exam results, view answer scripts

import streamlit as st
import pandas as pd
import mysql.connector
from fpdf import FPDF


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="examportal"
    )

def take_exam():
    st.title("Take Exam")
    st.write("This application is used to take the exam")
    st.write("Please enter the exam details")

    # Prompt user for exam ID
    exam_id = st.text_input("Enter exam ID")

    if exam_id:
        # Fetch questions from the database
        try:
            db = connect_to_database()
            cursor = db.cursor()
            cursor.execute("SELECT qid, qtext FROM theory WHERE examId=%s", (exam_id,))
            questions = cursor.fetchall()
        except mysql.connector.Error as e:
            st.error(f"Error fetching questions from database: {e}")
            return

        if questions:
            st.write(f"Number of questions: {len(questions)}")
            st.write("Please answer the following questions:")

            # Display each question and prompt for answer
            for qid, qtext in questions:
                st.write(f"Question {qid}: {qtext}")
                answer = st.text_area(f"Enter your answer for Question {qid}")

                # Store the answer or process it as needed
                # For now, we'll just print the answer
                st.write(f"Answer for Question {qid}: {answer}")
            

            # Add submit button
            if st.button("Submit"):
                # Convert answers to PDF using fpdf
                # Add your code here to convert answers to PDF using fpdf library
                # Example code using fpdf:
                # 
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for qid, qtext in questions:
                    pdf.cell(0, 10, f"Question {qid}: {qtext}", ln=True)
                    pdf.cell(0, 10, f"Answer for Question {qid}: {answer}", ln=True)
                pdf.output("answers.pdf")
                st.success("Answers submitted successfully. Your answers have been saved to answers.pdf")



        else:
            st.error("No questions found for the specified exam ID")
    else:
        st.warning("Please enter an exam ID")


def student_functions():
    st.sidebar.title("Student Functions")
    option = st.sidebar.radio("Select Option", ["Take Exam", "View Exam Results", "View Answer Scripts"])
    if option == "Take Exam":
        take_exam()
    elif option == "View Exam Results":
        view_exam_results()
    elif option == "View Answer Scripts":
        view_answer_scripts()

student_functions()