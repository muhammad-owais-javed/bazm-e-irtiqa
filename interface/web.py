import streamlit as st
import asyncio
import nest_asyncio

from agents.manager import manager_agent
from agents.frontend import frontend_agent_stream
from agents.database import database_agent_stream
from agents.backend import backend_agent_stream
from agents.qa import qa_agent_stream
from core.llm_client import MODEL_NAME, async_ask_agent_stream
from core.executor import execute_in_sandbox

nest_asyncio.apply()
st.set_page_config(page_title="Bazm-e-Irtiqa", page_icon="🤖", layout="wide")

if "fe_memory" not in st.session_state:
    st.session_state.fe_memory = []
    st.session_state.db_memory = []
    st.session_state.be_memory = []
    st.session_state.qa_memory = []
    st.session_state.chat_history = [] 
    st.session_state.artifacts = None

# Helper function to strip Markdown backticks for the Sandbox!
def extract_code(text):
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()

st.title("🤖 Bazm-e-Irtiqa Factory")
st.markdown(f"**Model:** `{MODEL_NAME}` | **Router:** Active | **Sandbox:** Monitored")
st.divider()

col1, col2 = st.columns([1, 1])

# --- RIGHT SIDE: Visual Sandbox ---
with col2:
    st.subheader("🖥️ Live Sandbox View")
    st.components.v1.iframe("http://localhost:6080/", height=600 )

# --- LEFT SIDE: Chat Interface ---
with col1:
    st.subheader("💬 Agent Chat")
    chat_container = st.container(height=500)
    
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # --- NEW ARTIFACT VIEWER (Tabs with Copy & Download) ---
    if st.session_state.artifacts:
        st.markdown("### 💾 Review & Download Artifacts")
        html_tab, sql_tab, py_tab = st.tabs(["🎨 index.html", "🗄️ schema.sql", "⚙️ app.py"])
        
        with html_tab:
            st.code(st.session_state.artifacts.get("html",""), language="html")
            st.download_button("📥 Download HTML", st.session_state.artifacts.get("html",""), file_name="index.html")
            
        with sql_tab:
            st.code(st.session_state.artifacts.get("sql",""), language="sql")
            st.download_button("📥 Download SQL", st.session_state.artifacts.get("sql",""), file_name="schema.sql")
            
        with py_tab:
            st.code(st.session_state.artifacts.get("py",""), language="python")
            st.download_button("📥 Download Python", st.session_state.artifacts.get("py",""), file_name="app.py")

# --- CHAT INPUT ---
if task := st.chat_input("📝 What would you like to build or discuss?"):
    st.session_state.chat_history.append({"role": "user", "content": task})
    
    with col1:
        with chat_container:
            with st.chat_message("user"):
                st.markdown(task)
            
            with st.chat_message("assistant"):
                async def run_workflow():
                    st.markdown("### 🧠 Manager Agent")
                    with st.spinner("Classifying task..."):
                        task_type = await manager_agent(task)
                    st.info(f"Task classified as: **{task_type}**")
                    
                    if task_type == "CHAT":
                        st.markdown("### 🤖 Assistant")
                        reply = st.write_stream(async_ask_agent_stream("General", "You are a helpful assistant.", task, st.session_state.be_memory))
                        return reply
                        
                    elif task_type in ["WEB_APP", "SCRIPT"]:
                        st.markdown("### 🎨 Frontend Agent")
                        ui_code = st.write_stream(frontend_agent_stream(task, st.session_state.fe_memory))
                        
                        st.markdown("### 🗄️ Database Agent")
                        db_schema = st.write_stream(database_agent_stream(task, st.session_state.db_memory))
                        
                        st.markdown("### ⚙️ Backend Agent")
                        server_code = st.write_stream(backend_agent_stream(ui_code, db_schema, st.session_state.be_memory))
                        
                        max_retries = 2
                        for attempt in range(max_retries):
                            st.markdown(f"### 🖥️ Sandbox Execution (Attempt {attempt+1})")
                            with st.spinner("Testing in VM..."):
                                # Extract pure python before executing!
                                clean_server_code = extract_code(server_code)
                                is_success, logs = execute_in_sandbox(clean_server_code)
                            
                            if is_success:
                                st.success("✅ App launched perfectly!")
                                break
                            else:
                                st.error("⚠️ Sandbox crashed! Sending logs to QA...")
                                st.code(logs, language="bash")
                                fix_prompt = f"The code crashed. Fix these errors:\n\n{logs}\n\nEnsure it runs on port 5000."
                                st.markdown("### ⚙️ Backend Agent (Fixing)")
                                server_code = st.write_stream(backend_agent_stream("Keep previous HTML", fix_prompt, st.session_state.be_memory))
                        
                        st.session_state.artifacts = {"html": extract_code(ui_code), "sql": extract_code(db_schema), "py": extract_code(server_code)}
                        return "Web App deployed to Sandbox. Artifacts ready."

                final_text = asyncio.run(run_workflow())
                st.session_state.chat_history.append({"role": "assistant", "content": final_text})
                st.rerun()
