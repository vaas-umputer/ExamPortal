#professor functions
#add a side panel on left and have options 
#options are : set question paper, view question paper, view exam results, view answer scripts

import streamlit as st
import setExam
import pandas as pd

def viewQuestionPaper():
    st.title("View Question Paper")
    st.write("This application is used to view the question paper")
    st.write("Please enter the exam id")
    exam_id = st.text_input("Enter exam id")
    if st.button("View Question Paper"):
        try:
            db = setExam.connect_to_database()
            cursor = db.cursor()
            cursor.execute("SELECT qid,qtext,qmarks FROM theory WHERE examId=%s", (exam_id,))
            result = cursor.fetchall()
            if result:
                st.write("Question Paper")
                df = pd.DataFrame(result, columns=["Question ID", "Question", "Marks"])
                #df=df.drop(df.iloc[:, 0:1], axis=1)
                st.write(df)  # Add index=False to remove row numbers
            else:
                st.error("No question paper found")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def professor_functions():
    st.sidebar.title("Professor Functions")
    option = st.sidebar.radio("Select Option", ["Set Question Paper", "View Question Paper", "View Exam Results", "View Answer Scripts"])
    if option == "Set Question Paper":
        setExam.setQuestionPaper()
    elif option == "View Question Paper":
        viewQuestionPaper()
    elif option == "View Exam Results":
        st.write("View Exam Results")
    elif option == "View Answer Scripts":
        st.write("View Answer Scripts")
    
    
professor_functions()