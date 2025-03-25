import streamlit as st
import pandas as pd

JOURNAL_DB = "data/journals.csv"
FEEDBACK_DB = "data/cse_feedback.csv"

def cse_review_dashboard():
    st.subheader("📊 Review Siri Solvers' Work")
    review_class_code = st.text_input("Enter Class Code to View Submissions")

    if review_class_code:
        if not os.path.exists(JOURNAL_DB):
            st.warning("No journal submissions found.")
            return
        
        journals = pd.read_csv(JOURNAL_DB)
        class_journals = journals[journals["Class Code"] == review_class_code]

        if class_journals.empty:
            st.warning("No journal entries found for this class.")
            return

        for _, row in class_journals.iterrows():
            st.write(f"📖 **{row['Task Name']}** - Student Submission")
            st.write(f"✏ {row['Journal Entry']}")

            # CSE Scoring & Feedback
            score = st.slider(f"Score for {row['Task Name']} (1-5)", 1, 5, 3)
            feedback = st.text_area(f"CSE Comments for {row['Task Name']}")
            
            if st.button(f"Submit Feedback for {row['Task Name']}"):
                if not os.path.exists(FEEDBACK_DB):
                    df = pd.DataFrame(columns=["Class Code", "Task Name", "Journal Entry", "Score", "CSE Comments"])
                else:
                    df = pd.read_csv(FEEDBACK_DB)
                
                new_entry = pd.DataFrame([[row["Class Code"], row["Task Name"], row["Journal Entry"], score, feedback]],
                                         columns=["Class Code", "Task Name", "Journal Entry", "Score", "CSE Comments"])
                df = pd.concat([df, new_entry])
                df.to_csv(FEEDBACK_DB, index=False)
                st.success(f"✅ Feedback submitted for {row['Task Name']}!")

