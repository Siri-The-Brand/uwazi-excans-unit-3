import streamlit as st
import pandas as pd
import os
import random

# Database paths
STUDENT_DB = "data/students.csv"
TASK_PROGRESS_DB = "data/task_progress.csv"
TASKS_DB = "data/unit3_tasks.csv"  # ✅ Add the main tasks CSV
LEADERBOARD_DB = "data/leaderboard.csv"
ACHIEVEMENTS_DB = "data/achievements.csv"
DAILY_CHALLENGES_DB = "data/daily_challenges.csv"

def load_student_data():
    """Load student profiles"""
    return pd.read_csv(STUDENT_DB) if os.path.exists(STUDENT_DB) else pd.DataFrame()

def load_tasks():
    """Load all tasks"""
    return pd.read_csv(TASKS_DB) if os.path.exists(TASKS_DB) else pd.DataFrame()

def load_student_tasks(student_id):
    """Load tasks assigned to a specific student"""
    tasks = pd.read_csv(TASK_PROGRESS_DB) if os.path.exists(TASK_PROGRESS_DB) else pd.DataFrame()
    return tasks[tasks["Student ID"] == student_id]

def update_task_completion(student_id, task_name):
    """Mark a task as completed"""
    if os.path.exists(TASK_PROGRESS_DB):
        tasks = pd.read_csv(TASK_PROGRESS_DB)
        tasks.loc[(tasks["Student ID"] == student_id) & (tasks["Task Name"] == task_name), "Task Completed"] = "Yes"
        tasks.to_csv(TASK_PROGRESS_DB, index=False)
        return True
    return False

def student_dashboard():
    st.subheader("🎮 Welcome to Your Siri Solver Dashboard")

    # Student Login using Student ID
    student_id = st.text_input("Enter Your Student ID")

    if student_id:
        students = load_student_data()
        student_row = students[students["Student ID"] == student_id]

        if student_row.empty:
            st.error("Invalid Student ID! Please check with your CSE.")
        else:
            student_name = student_row["Name"].values[0]
            xp_points = int(student_row["XP Points"].values[0])
            level = int(student_row["Level"].values[0])
            umeme_points = int(student_row["Umeme Points"].values[0])

            # Display Profile & Achievements
            st.write(f"🧑‍🎓 **{student_name}** | 🎯 XP: {xp_points} | ⚡ Umeme Points: {umeme_points} | 🏆 Level: {level}")

            # 📌 **Display Assigned Tasks**
            st.subheader("📋 Your Tasks")
            student_tasks = load_student_tasks(student_id)

            if not student_tasks.empty:
                for _, row in student_tasks.iterrows():
                    task_name = row["Task Name"]
                    completed = row["Task Completed"]

                    st.write(f"**{task_name}** - {'✅ Completed' if completed == 'Yes' else '❌ Not Completed'}")

                    # ✅ Button to mark task as completed
                    if completed == "No":
                        if st.button(f"✔️ Complete {task_name}"):
                            update_task_completion(student_id, task_name)
                            st.success(f"🎉 Task '{task_name}' marked as completed!")
                            st.experimental_rerun()

            else:
                st.info("No tasks assigned yet!")

            # 🎲 **Daily Challenges**
            st.subheader("🎲 Daily Challenge")
            daily_challenges = pd.read_csv(DAILY_CHALLENGES_DB) if os.path.exists(DAILY_CHALLENGES_DB) else pd.DataFrame()

            if not daily_challenges.empty:
                daily_challenge = daily_challenges.sample(1).iloc[0]
                st.write(f"**{daily_challenge['Description']}**")
                if st.button("Complete Daily Challenge"):
                    xp_reward = int(daily_challenge["XP Reward"])
                    umeme_reward = int(daily_challenge["Umeme Reward"])
                    st.success(f"✅ Challenge completed! +{xp_reward} XP, +{umeme_reward} ⚡Umeme Points!")

            else:
                st.warning("No daily challenges available.")

            # 🎤 **File Upload for Journals**
            st.subheader("📤 Upload Journal Submission")
            uploaded_file = st.file_uploader("Upload Your Work (Image, Audio, Video)", type=["jpg", "png", "mp3", "mp4"])

            if uploaded_file:
                file_path = f"uploads/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success("File uploaded successfully! 🎉")

            # 📊 **AI Feedback Placeholder**
            st.subheader("🤖 AI-Based Feedback (Coming Soon)")
            st.write("Your work will be reviewed by AI and a CSE for feedback.")

            # 🏆 **Leaderboard**
            st.subheader("🏅 Class Leaderboard")
            leaderboard = pd.read_csv(LEADERBOARD_DB) if os.path.exists(LEADERBOARD_DB) else pd.DataFrame()
            if not leaderboard.empty:
                st.write("🔝 **Top 5 XP Earners**")
                top_xp = leaderboard.sort_values("XP Points", ascending=False).head(5)
                st.dataframe(top_xp)

                st.write("⚡ **Top 5 Umeme Earners**")
                top_umeme = leaderboard.sort_values("Umeme Points", ascending=False).head(5)
                st.dataframe(top_umeme)
            else:
                st.info("No leaderboard data available yet.")

