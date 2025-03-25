import streamlit as st
import random

def start_ar_task(task_name):
    """Show AR-based interactive challenge"""
    challenges = {
        "Eco-Creators": "Find and scan 3 different types of leaves 🌿",
        "Sustainable Garden": "Identify and categorize 2 plants based on size 🏡",
        "Incubator Innovators": "Record temperature changes in an incubator 📡"
    }
    
    challenge = challenges.get(task_name, "No AR task available.")
    st.info(challenge)

    if st.button("Mark as Complete"):
        st.success("✅ AR task completed! 🎉")

