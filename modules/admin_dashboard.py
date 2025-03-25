import streamlit as st
import pandas as pd
import os

ADMIN_DB = "data/admin_dashboard.csv"

def admin_dashboard():
    st.subheader("📊 Admin Dashboard")

    # Load data
    df = pd.read_csv(ADMIN_DB) if os.path.exists(ADMIN_DB) else pd.DataFrame()

    if df.empty:
        st.warning("No class data found.")
    else:
        st.write(df)

        # Show top-performing classes
        st.subheader("🏆 Top Classes")
        top_classes = df.sort_values("Class XP", ascending=False).head(3)
        st.write(top_classes)

        # Average class completion rates
        avg_completion = df["Avg Completion Rate"].mean()
        st.write(f"📈 **Average Completion Rate:** {avg_completion:.2f}%")

