import streamlit as st
import mysql.connector

# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="examportal"
    )

def setQuestionPaper():
    st.title("Set Question Paper")
    st.write("This application is used to set the question paper")
    st.write("Please enter the question details")

    # Prompt user for exam id
    exam_id = st.text_input("Enter exam id")

    # Lists to store questions and marks
    questions = []
    marks_list = []

    num_questions = st.number_input("Number of Questions", min_value=1, step=1, value=1)

    for i in range(num_questions):
        st.write(f"Question {i+1}")
        col1, col2 = st.columns([3, 1])
        with col1:
            question = st.text_input(f"Enter question {i+1}")
        with col2:
            marks = st.text_input(f"Marks", key=f"marks_{i}", value="", max_chars=3)
            marks_list.append(marks)

        questions.append(question)

    # Add button to submit questions
    if st.button("Submit"):
        try:
            db = connect_to_database()
            cursor = db.cursor()
            counter = 1
            for question, marks in zip(questions, marks_list):
                qid = counter
                if not question:  # Check if question text is empty
                    st.error("Question text cannot be empty")
                    continue  # Skip this iteration and continue with the next question
                if not marks:  # Check if marks is empty
                    st.error("Marks cannot be empty")
                    continue  # Skip this iteration and continue with the next question

                # Validate marks to ensure it's an integer before inserting into the database
                try:
                    marks = int(marks)
                except ValueError:
                    st.error("Marks must be a valid integer")
                    continue
                cursor.execute("INSERT INTO theory (qid, qtext, qmarks, examId) VALUES (%s, %s, %s, %s)",
                               (qid, question, marks, exam_id))
                counter += 1
            db.commit()
            st.write("Questions added successfully")
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

setQuestionPaper()
