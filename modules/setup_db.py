import pandas as pd
import os

# Define database directory & ensure it exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)  # Create 'data' folder if missing

# Define database file paths
STUDENT_DB = os.path.join(DATA_DIR, "students.csv")
TASK_PROGRESS_DB = os.path.join(DATA_DIR, "task_progress.csv")
ADMIN_DB = os.path.join(DATA_DIR, "admin_dashboard.csv")
LEADERBOARD_DB = os.path.join(DATA_DIR, "leaderboard.csv")
ACHIEVEMENTS_DB = os.path.join(DATA_DIR, "achievements.csv")
DAILY_CHALLENGES_DB = os.path.join(DATA_DIR, "daily_challenges.csv")
CLASSES_DB = os.path.join(DATA_DIR, "classes.csv")
# Define data structures
DATA_STRUCTURES = {
    "students": {
        "Student ID": [], "Name": [], "Class Code": [],
        "Avatar": [], "Completed Tasks": [], "XP Points": [],
        "Level": [], "Umeme Points": [], "Badges": []
    },
    "task_progress": {
        "Student ID": [], "Task Name": [], "AR Task Completed": [],
        "File Submission": [], "Score": [], "Feedback": []
    },
    "admin_dashboard": {
        "Class Code": [], "Total Students": [], "Avg Completion Rate": [],
        "Top Performer": [], "Class XP": []
    },
    "leaderboard": {
        "Student ID": [], "Name": [], "XP Points": [], "Level": [], "Umeme Points": []
    },
    "achievements": {
        "Student ID": [], "Achievement Badge": [], "Date Earned": []
    },
    "daily_challenges": {
        "Challenge ID": [], "Description": [], "XP Reward": [], "Umeme Reward": [], "Status": []
    }
}

# Create CSV files if they don’t exist
for db_name, structure in DATA_STRUCTURES.items():
    file_path = os.path.join(DATA_DIR, f"{db_name}.csv")

    if not os.path.exists(file_path):
        df = pd.DataFrame(structure)
        df.to_csv(file_path, index=False)
        print(f"✅ {file_path} created!")

print("✅ Database setup completed successfully!")

