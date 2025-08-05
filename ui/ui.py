# ui.py
from main_agent import run_agent
import streamlit as st

st.title("SmartLINK Agent UI")

user_question = st.text_input("Ask your question about users:")

if st.button("Submit") and user_question:
    with st.spinner("Getting answer..."):
        try:
            answer = run_agent(user_question)
            st.write("**Answer:**")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")
