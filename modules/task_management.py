import streamlit as st
import pandas as pd
import os
import random

# Database paths
STUDENT_DB = "data/students.csv"
TASK_PROGRESS_DB = "data/task_progress.csv"
TASKS_DB = "data/unit3_tasks.csv"
LEADERBOARD_DB = "data/leaderboard.csv"
ACHIEVEMENTS_DB = "data/achievements.csv"
DAILY_CHALLENGES_DB = "data/daily_challenges.csv"
JOURNAL_DB = "data/journals.csv"

# Ensure required folders exist
UPLOADS_FOLDER = "uploads"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# Ensure journal database exists
if not os.path.exists(JOURNAL_DB):
    pd.DataFrame(columns=["Student ID", "Task Name", "Journal Entry", "File Submission"]).to_csv(JOURNAL_DB, index=False)

def load_student_data():
    """Load student profiles"""
    return pd.read_csv(STUDENT_DB) if os.path.exists(STUDENT_DB) else pd.DataFrame()

def load_daily_challenges():
    """Load daily challenge data"""
    return pd.read_csv(DAILY_CHALLENGES_DB) if os.path.exists(DAILY_CHALLENGES_DB) else pd.DataFrame()

def load_leaderboard():
    """Load leaderboard data"""
    return pd.read_csv(LEADERBOARD_DB) if os.path.exists(LEADERBOARD_DB) else pd.DataFrame()

def update_leaderboard():
    """Update leaderboard with student rankings based on XP and Umeme Points"""
    students = load_student_data()

    if not students.empty:
        leaderboard = students[["Student ID", "Name", "XP Points", "Umeme Points"]]
        leaderboard.to_csv(LEADERBOARD_DB, index=False)

def save_journal_entry(student_id, task_name, journal_text, file_submission=None):
    """Save journal text or file submission"""
    journals = pd.read_csv(JOURNAL_DB) if os.path.exists(JOURNAL_DB) else pd.DataFrame()

    # Remove existing entry for the same task
    journals = journals[~((journals["Student ID"] == student_id) & (journals["Task Name"] == task_name))]

    # Add new entry
    new_entry = pd.DataFrame([[student_id, task_name, journal_text, file_submission]],
                             columns=["Student ID", "Task Name", "Journal Entry", "File Submission"])
    journals = pd.concat([journals, new_entry])
    journals.to_csv(JOURNAL_DB, index=False)

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

            # 🎲 **Daily Challenges**
            st.subheader("🎲 Daily Challenge")
            daily_challenges = load_daily_challenges()

            if not daily_challenges.empty:
                daily_challenge = daily_challenges.sample(1).iloc[0]  # Pick a random challenge
                st.write(f"**Challenge:** {daily_challenge['Description']}")

                if st.button("✅ Complete Daily Challenge"):
                    xp_reward = int(daily_challenge["XP Reward"])
                    umeme_reward = int(daily_challenge["Umeme Reward"])

                    # Update student's XP & Umeme Points
                    students.loc[students["Student ID"] == student_id, "XP Points"] += xp_reward
                    students.loc[students["Student ID"] == student_id, "Umeme Points"] += umeme_reward
                    students.to_csv(STUDENT_DB, index=False)

                    # Update leaderboard
                    update_leaderboard()

                    st.success(f"🎉 Challenge completed! +{xp_reward} XP, +{umeme_reward} ⚡Umeme Points!")
                    st.rerun()  # Refresh UI

            else:
                st.warning("⚠️ No daily challenges available.")

            # 🎤 **Journal Submission Section**
            st.subheader("📖 Submit Your Journal Entry")

            # Select Task for Journal Submission
            student_tasks = pd.read_csv(TASK_PROGRESS_DB) if os.path.exists(TASK_PROGRESS_DB) else pd.DataFrame()
            student_tasks = student_tasks[student_tasks["Student ID"] == student_id]

            if not student_tasks.empty:
                selected_task = st.selectbox("Select a Task", student_tasks["Task Name"].unique())

                # Show Existing Submission
                journals = pd.read_csv(JOURNAL_DB) if os.path.exists(JOURNAL_DB) else pd.DataFrame()
                existing_entry = journals[(journals["Student ID"] == student_id) & (journals["Task Name"] == selected_task)]

                if not existing_entry.empty:
                    st.write("✅ **Your Previous Submission:**")
                    st.write(f"✏ **Journal Entry:** {existing_entry['Journal Entry'].values[0]}")

                # Submit a New Journal Entry
                st.subheader("✏ Text-Based Submission")
                journal_text = st.text_area("Write your journal entry here...")

                # Upload File (Optional)
                st.subheader("📤 Upload File Submission (Optional)")
                uploaded_file = st.file_uploader("Upload an image, audio, or video", type=["jpg", "png", "mp3", "mp4"])

                file_path = None
                if uploaded_file:
                    file_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                # Submit Button
                if st.button("Submit Journal Entry"):
                    save_journal_entry(student_id, selected_task, journal_text, file_path)
                    st.success(f"✅ Journal entry submitted for '{selected_task}'!")
                    st.rerun()

            else:
                st.warning("⚠️ No tasks assigned yet. Please wait for assignments.")

            # 🏆 **Leaderboard**
            st.subheader("🏅 Class Leaderboard")
            leaderboard = load_leaderboard()

            if not leaderboard.empty:
                st.write("🔝 **Top 5 XP Earners**")
                top_xp = leaderboard.sort_values("XP Points", ascending=False).head(5)
                st.dataframe(top_xp)

                st.write("⚡ **Top 5 Umeme Earners**")
                top_umeme = leaderboard.sort_values("Umeme Points", ascending=False).head(5)
                st.dataframe(top_umeme)
            else:
                st.info("No leaderboard data available yet.")

