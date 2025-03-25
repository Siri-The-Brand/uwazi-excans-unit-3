import streamlit as st
from modules.class_management import create_class_ui, join_class_ui
from modules.task_management import student_dashboard
from modules.admin_dashboard import admin_dashboard
from modules.cse_dashboard import cse_dashboard  # ✅ Updated to import CSE Dashboard
from modules.review_system import cse_review_dashboard  # ✅ Separate CSE review system

st.title("🎵 Unit 3: Music in Nature - Class System")

# Sidebar Navigation
page = st.sidebar.selectbox("Navigation", [
    "📚 Create a Class",
    "👨‍🏫 Join a Class",
    "🎮 Student Dashboard",
    "📊 Admin Dashboard",
    "📑 CSE Task Management & Review"
])

if page == "📚 Create a Class":
    create_class_ui()
elif page == "👨‍🏫 Join a Class":
    join_class_ui()
elif page == "🎮 Student Dashboard":
    student_dashboard()
elif page == "📊 Admin Dashboard":
    admin_dashboard()
elif page == "📑 CSE Task Management & Review":
    cse_dashboard()

