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
DAILY_SUBMISSIONS_DB = "data/daily_submissions.csv"  # ✅ New DB to store proof of challenge completion

# Ensure required folders exist
UPLOADS_FOLDER = "uploads"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# Ensure daily submission database exists
if not os.path.exists(DAILY_SUBMISSIONS_DB):
    pd.DataFrame(columns=["Student ID", "Challenge ID", "Submission Text", "File Submission", "Reviewed"]).to_csv(DAILY_SUBMISSIONS_DB, index=False)

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

def save_daily_submission(student_id, challenge_id, submission_text, file_submission=None):
    """Save student's proof of challenge completion"""
    submissions = pd.read_csv(DAILY_SUBMISSIONS_DB) if os.path.exists(DAILY_SUBMISSIONS_DB) else pd.DataFrame()

    # Remove existing submission if present
    submissions = submissions[~((submissions["Student ID"] == student_id) & (submissions["Challenge ID"] == challenge_id))]

    # Add new entry
    new_entry = pd.DataFrame([[student_id, challenge_id, submission_text, file_submission, "Pending"]],
                             columns=["Student ID", "Challenge ID", "Submission Text", "File Submission", "Reviewed"])
    submissions = pd.concat([submissions, new_entry])
    submissions.to_csv(DAILY_SUBMISSIONS_DB, index=False)

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
                challenge_id = daily_challenge["Challenge ID"]
                st.write(f"**Challenge:** {daily_challenge['Description']}")

                # Check if student has already submitted proof
                submissions = pd.read_csv(DAILY_SUBMISSIONS_DB) if os.path.exists(DAILY_SUBMISSIONS_DB) else pd.DataFrame()
                existing_submission = submissions[(submissions["Student ID"] == student_id) & (submissions["Challenge ID"] == challenge_id)]

                if not existing_submission.empty:
                    st.success("✅ Submission received! Waiting for review.")
                else:
                    # Submission Section
                    st.subheader("📤 Submit Proof of Completion")
                    submission_text = st.text_area("Describe how you completed the challenge")

                    uploaded_file = st.file_uploader("Upload an image, audio, or video (Optional)", type=["jpg", "png", "mp3", "mp4"])
                    file_path = None

                    if uploaded_file:
                        file_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                    # Submit Button
                    if st.button("Submit Challenge Proof"):
                        if submission_text or file_path:
                            save_daily_submission(student_id, challenge_id, submission_text, file_path)
                            st.success("✅ Submission recorded! Awaiting review.")
                            st.rerun()
                        else:
                            st.warning("⚠️ Please provide either a text entry or a file submission.")

            else:
                st.warning("⚠️ No daily challenges available.")

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

