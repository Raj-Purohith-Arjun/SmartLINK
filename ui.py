import streamlit as st
from agent.main_agent import run_agent

st.set_page_config(page_title="SmartLINK Agent", page_icon="🧠")
st.title("🤖 SmartLINK Agent")
st.markdown("Ask questions about your **users** database.")

user_input = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = run_agent(user_input)
                st.success(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")
