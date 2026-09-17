import streamlit as st
from agents.frontend import frontend_agent
from agents.backend import backend_agent
from core.llm_client import MODEL_NAME

# Configure the page
st.set_page_config(page_title="Bazm-e-Irtiqa", page_icon="🤖", layout="centered")

st.title("🤖 Bazm-e-Irtiqa Factory")
st.markdown(f"**Active AI Model:** `{MODEL_NAME}`")
st.divider()

# User Input
task = st.text_area("📝 What would you like the agents to build?", 
                    placeholder="e.g., Create a beautiful 'Hello World' landing page with a dark mode theme.")

if st.button("🚀 Start Production", type="primary"):
    if not task.strip():
        st.warning("Please enter a task first!")
    else:
        # Step 1: Frontend Agent
        with st.spinner("🎨 Frontend Agent is designing the UI..."):
            ui_code = frontend_agent(task)
            st.success("Frontend Agent completed the UI!")
            with st.expander("🔍 View Frontend Output (HTML)"):
                st.code(ui_code, language='html')
        
        # Step 2: Backend Agent
        with st.spinner("⚙️ Backend Agent is building the server..."):
            server_code = backend_agent(ui_code)
            st.success("Backend Agent completed the server!")
            with st.expander("🔍 View Backend Output (Python)"):
                st.code(server_code, language='python')
        
        # Final Output
        st.divider()
        st.subheader("🎉 Final Coordinated Output")
        st.code(server_code, language='python')
