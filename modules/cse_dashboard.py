import streamlit as st
import pandas as pd
import os

# Database paths
CLASS_DB = "data/classes.csv"
STUDENT_DB = "data/students.csv"
TASKS_DB = "data/unit3_tasks.csv"  # ✅ Tasks become the class schedule
TASK_PROGRESS_DB = "data/task_progress.csv"

# Ensure required databases exist
def load_classes():
    return pd.read_csv(CLASS_DB) if os.path.exists(CLASS_DB) else pd.DataFrame()

def load_students():
    return pd.read_csv(STUDENT_DB) if os.path.exists(STUDENT_DB) else pd.DataFrame()

def load_tasks():
    return pd.read_csv(TASKS_DB) if os.path.exists(TASKS_DB) else pd.DataFrame()

def assign_task(student_id, task_name):
    """Assign a task to a student"""
    if not os.path.exists(TASK_PROGRESS_DB):
        df = pd.DataFrame(columns=["Student ID", "Task Name", "Task Completed"])
    else:
        df = pd.read_csv(TASK_PROGRESS_DB)

    new_entry = pd.DataFrame([[student_id, task_name, "No"]], columns=["Student ID", "Task Name", "Task Completed"])
    df = pd.concat([df, new_entry])
    df.to_csv(TASK_PROGRESS_DB, index=False)
    return True

def cse_dashboard():
    st.subheader("📚 CSE Dashboard - Manage Classes")

    # Select a class
    classes = load_classes()
    if classes.empty:
        st.warning("No classes found! Please create a class first.")
        return
    
    class_code = st.selectbox("Select a Class", classes["Class Code"].unique())
    class_info = classes[classes["Class Code"] == class_code].iloc[0]
    class_name = class_info["Class Name"]
    st.write(f"📌 Managing **{class_name}**")

    # View Student List
    st.subheader("👥 Class Students")
    students = load_students()
    class_students = students[students["Class Code"] == class_code]
    
    if class_students.empty:
        st.warning("No students have joined this class yet.")
    else:
        st.dataframe(class_students[["Student ID", "Name", "XP Points", "Level", "Umeme Points"]])

    # View & Assign Tasks
    st.subheader("📋 Assign Tasks")
    tasks = load_tasks()
    
    if tasks.empty:
        st.warning("No tasks available!")
    else:
        task_name = st.selectbox("Select a Task", tasks["Task Name"].unique())
        student_id = st.selectbox("Assign to Student", class_students["Student ID"].unique()) if not class_students.empty else None

        if student_id and st.button("Assign Task"):
            if assign_task(student_id, task_name):
                st.success(f"✅ Task '{task_name}' assigned to {student_id}!")

    # **NEW: View Class Schedule from `unit3_tasks.csv`**
    st.subheader("📅 Class Schedule (Unit 3 Tasks)")
    
    if tasks.empty:
        st.warning("No tasks found for this unit!")
    else:
        st.dataframe(tasks[["Day", "Task Name", "Task Description", "Resources"]])  # ✅ Shows key task details

