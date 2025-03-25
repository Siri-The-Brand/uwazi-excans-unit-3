import streamlit as st
import pandas as pd
import os
import random
import string

CLASS_DB = "data/classes.csv"
STUDENT_DB = "data/students.csv"

# Ensure CSV files exist before accessing them
for db in [CLASS_DB, STUDENT_DB]:
    if not os.path.exists(db):
        df = pd.DataFrame(columns=["Class Name", "CSE Name", "Class Code"]) if db == CLASS_DB else \
             pd.DataFrame(columns=["Student ID", "Name", "Class Code", "Avatar", "Completed Tasks", "XP Points", "Level", "Umeme Points", "Badges"])
        df.to_csv(db, index=False)

def generate_class_code():
    """Generate a 6-character random class code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_student_id():
    """Generate a unique 8-character Student ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def save_class(class_name, cse_name):
    """Save class details with a unique class code."""
    class_code = generate_class_code()
    df = pd.DataFrame([[class_name, cse_name, class_code]], columns=["Class Name", "CSE Name", "Class Code"])
    
    # Ensure file exists before reading
    if not os.path.exists(CLASS_DB):
        df.to_csv(CLASS_DB, index=False)
    else:
        df.to_csv(CLASS_DB, mode='a', header=False, index=False)

    return class_code

def create_class_ui():
    """Streamlit UI for CSE to create a new class."""
    st.subheader("📚 Create a New Class")
    class_name = st.text_input("Class Name")
    cse_name = st.text_input("Your Name (CSE)")
    
    if st.button("Create Class"):
        if class_name and cse_name:
            code = save_class(class_name, cse_name)
            st.success(f"Class Created! Share this code with students: {code}")
        else:
            st.error("Please enter all fields.")

def join_class_ui():
    """Streamlit UI for students to join a class."""
    st.subheader("🎓 Join a Class")
    student_name = st.text_input("Your Name")
    class_code = st.text_input("Enter Class Code")

    if st.button("Join Class"):
        if student_name and class_code:
            # Load class data
            classes = pd.read_csv(CLASS_DB)
            if class_code not in classes["Class Code"].values:
                st.error("Invalid Class Code! Please check with your CSE.")
                return
            
            # Generate unique Student ID
            student_id = generate_student_id()

            # Load students database
            students = pd.read_csv(STUDENT_DB)

            # Ensure student ID is unique
            while student_id in students["Student ID"].values:
                student_id = generate_student_id()

            # Add new student entry
            new_student = pd.DataFrame([[student_id, student_name, class_code, "👤", 0, 0, 1, 0, ""]],
                                       columns=["Student ID", "Name", "Class Code", "Avatar", "Completed Tasks", "XP Points", "Level", "Umeme Points", "Badges"])
            students = pd.concat([students, new_student])
            students.to_csv(STUDENT_DB, index=False)

            st.success(f"🎉 You have joined the class! Your Student ID is: **{student_id}**")
            st.info("Please **save your Student ID** for logging in later.")
        else:
            st.error("Please enter both your name and the class code.")

