import streamlit as st
import asyncio
from agents.frontend import frontend_agent_stream
from agents.database import database_agent_stream
from agents.backend import backend_agent_stream
from agents.qa import qa_agent_stream
from core.llm_client import MODEL_NAME
import nest_asyncio
nest_asyncio.apply()

from core.executor import execute_in_sandbox

# Changed layout to "wide" 
st.set_page_config(page_title="Bazm-e-Irtiqa", page_icon="🤖", layout="wide")

if "fe_memory" not in st.session_state:
    st.session_state.fe_memory = []
    st.session_state.db_memory = []
    st.session_state.be_memory = []
    st.session_state.qa_memory = []
    st.session_state.chat_history = [] 

st.title("🤖 Bazm-e-Irtiqa Factory")
st.markdown(f"**Active AI Model:** `{MODEL_NAME}` | **Features:** Streaming, QA Loop & Visual Sandbox")
st.divider()

# Create a two-column layout
col1, col2 = st.columns([1, 1]) # 50/50 split

# --- RIGHT SIDE: The Visual Sandbox ---
with col2:
    st.subheader("🖥️ Live Sandbox View")
    # Removed /vnc.html from the URL
    st.components.v1.iframe("http://localhost:6080/", height=700 )

# --- LEFT SIDE: The Agent Chat ---
with col1:
    st.subheader("💬 Agent Chat")            
    
    # Create a container for the chat area inside the column
    chat_container = st.container(height=600)
    
    with chat_container:
        # Display previous chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        
        if task := st.chat_input("📝 What would you like the agents to build or change?"):
            
            st.session_state.chat_history.append({"role": "user", "content": task})
            with st.chat_message("user"):
                st.markdown(task)

            with st.chat_message("assistant"):
                async def run_workflow():
                   
                    st.markdown("### 🎨 Frontend Agent")
                    ui_code = st.write_stream(frontend_agent_stream(task, st.session_state.fe_memory))
                    
                    st.markdown("### 🗄️ Database Agent")
                    db_schema = st.write_stream(database_agent_stream(task, st.session_state.db_memory))
                    
                    st.markdown("### ⚙️ Backend Agent")
                    server_code = st.write_stream(backend_agent_stream(ui_code, db_schema, st.session_state.be_memory))
                    
                    st.markdown("### 🖥️ Executing in Sandbox...")
                    with st.spinner("Injecting code and opening Firefox in the Sandbox..."):
                        is_success, execution_logs = execute_in_sandbox(server_code)
                        
                        if is_success:
                            st.success("✅ App launched in the Visual Sandbox! Look at the screen on the right!")
                        else:
                            st.error("⚠️ App crashed on launch. Sending logs to QA...")
                            # Append the crash logs to the code so the QA agent sees them!
                            server_code += f"\n\n# ERROR LOGS FROM EXECUTION:\n# {execution_logs}"
                            
                    max_retries = 2
                    for attempt in range(max_retries):
                        st.markdown(f"### 🕵️ QA Agent (Attempt {attempt+1})")
                        qa_feedback = st.write_stream(qa_agent_stream(server_code, st.session_state.qa_memory))
                        
                        if "PASS" in qa_feedback.upper():
                            st.success("✅ QA Passed! Code is ready.")
                            break
                        else:
                            st.warning("⚠️ QA found issues. Backend is fixing...")
                            fix_prompt = f"The QA Agent found these issues. Please fix them and return ONLY the updated Python code:\n\n{qa_feedback}"
                            
                            st.markdown("### ⚙️ Backend Agent (Fixing)")
                            server_code = st.write_stream(backend_agent_stream("Keep previous HTML", fix_prompt, st.session_state.be_memory))
                    
                    return server_code

                final_code = asyncio.run(run_workflow())
                st.session_state.chat_history.append({"role": "assistant", "content": final_code})
