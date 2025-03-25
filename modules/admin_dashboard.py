import streamlit as st
import pandas as pd
import os

# Database paths
ADMIN_DB = "data/admin_dashboard.csv"
CLASS_DB = "data/classes.csv"
STUDENT_DB = "data/students.csv"
DAILY_SUBMISSIONS_DB = "data/daily_submissions.csv"

def admin_dashboard():
    st.subheader("📊 Admin Dashboard")

    # Load Class Data
    df_classes = pd.read_csv(CLASS_DB) if os.path.exists(CLASS_DB) else pd.DataFrame()
    df_students = pd.read_csv(STUDENT_DB) if os.path.exists(STUDENT_DB) else pd.DataFrame()
    df_admin = pd.read_csv(ADMIN_DB) if os.path.exists(ADMIN_DB) else pd.DataFrame()
    df_submissions = pd.read_csv(DAILY_SUBMISSIONS_DB) if os.path.exists(DAILY_SUBMISSIONS_DB) else pd.DataFrame()

    # Show class overview
    if df_classes.empty:
        st.warning("⚠️ No class data found. Ensure classes have been created.")
    else:
        st.subheader("🏫 **All Classes Overview**")
        st.dataframe(df_classes)

    # Show student stats per class
    if df_students.empty:
        st.warning("⚠️ No student data available.")
    else:
        st.subheader("📚 **Student Statistics**")
        students_by_class = df_students.groupby("Class Code").agg(
            Total_Students=("Student ID", "count"),
            Avg_XP=("XP Points", "mean"),
            Avg_Umeme=("Umeme Points", "mean"),
        ).reset_index()

        st.dataframe(students_by_class)

    # Show leaderboard for top classes
    if not df_admin.empty:
        st.subheader("🏆 **Top-Performing Classes**")
        top_classes = df_admin.sort_values("Class XP", ascending=False).head(3)
        st.dataframe(top_classes)

        # Average class completion rates
        avg_completion = df_admin["Avg Completion Rate"].mean()
        st.write(f"📈 **Average Completion Rate:** {avg_completion:.2f}%")

    # ✅ **Pending Daily Challenge Reviews**
    st.subheader("📌 Review Challenge Submissions")
    
    if df_submissions.empty:
        st.info("No pending submissions.")
    else:
        pending_submissions = df_submissions[df_submissions["Reviewed"] == "Pending"]

        if pending_submissions.empty:
            st.success("🎉 All challenge submissions have been reviewed!")
        else:
            for index, row in pending_submissions.iterrows():
                st.write(f"🧑‍🎓 **Student ID:** {row['Student ID']}")
                st.write(f"📌 **Challenge ID:** {row['Challenge ID']}")
                st.write(f"✏ **Submission:** {row['Submission Text']}")

                if pd.notna(row["File Submission"]) and row["File Submission"]:
                    st.write(f"📎 **File Submission:** {row['File Submission']}")
                    if row["File Submission"].endswith(('.mp3', '.wav')):
                        st.audio(row["File Submission"])
                    else:
                        st.image(row["File Submission"])

                # Approve or Reject Buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve {row['Challenge ID']}", key=f"approve_{index}"):
                        df_submissions.loc[df_submissions.index == index, "Reviewed"] = "Approved"
                        df_submissions.to_csv(DAILY_SUBMISSIONS_DB, index=False)
                        st.success(f"🎉 Challenge {row['Challenge ID']} approved!")

                with col2:
                    if st.button(f"❌ Reject {row['Challenge ID']}", key=f"reject_{index}"):
                        df_submissions.loc[df_submissions.index == index, "Reviewed"] = "Rejected"
                        df_submissions.to_csv(DAILY_SUBMISSIONS_DB, index=False)
                        st.warning(f"🚨 Challenge {row['Challenge ID']} rejected.")

    st.write("---")
    st.info("Admins can review challenge submissions, monitor student progress, and track class performance.")

