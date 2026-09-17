import streamlit as st
import asyncio
from agents.frontend import frontend_agent_stream
from agents.database import database_agent_stream
from agents.backend import backend_agent_stream
from agents.qa import qa_agent_stream
from core.llm_client import MODEL_NAME

st.set_page_config(page_title="Bazm-e-Irtiqa", page_icon="🤖", layout="centered")

# 1. Initialize Memory in Streamlit Session State
if "fe_memory" not in st.session_state:
    st.session_state.fe_memory = None
    st.session_state.db_memory = None
    st.session_state.be_memory = None
    st.session_state.qa_memory = None
    st.session_state.chat_history = [] # Stores the UI chat logs

st.title("🤖 Bazm-e-Irtiqa Factory")
st.markdown(f"**Active AI Model:** `{MODEL_NAME}` | **Features:** Parallel Execution & QA Loop")
st.divider()

# 2. Display previous chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Chat Input (UPDATE: This replaces the old text_area and button)
if task := st.chat_input("📝 What would you like the agents to build or change?"):
    
    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": task})
    with st.chat_message("user"):
        st.markdown(task)

    # AI Processing Block
    with st.chat_message("assistant"):
        status_text = st.empty()
        
    with st.chat_message("assistant"):
        async def run_workflow():
            # STEP 1: FRONTEND
            st.markdown("### 🎨 Frontend Agent")
            ui_code = await st.write_stream(frontend_agent_stream(task, st.session_state.fe_memory))
            
            # STEP 2: DATABASE
            st.markdown("### 🗄️ Database Agent")
            db_schema = await st.write_stream(database_agent_stream(task, st.session_state.db_memory))
            
            # STEP 3: BACKEND
            st.markdown("### ⚙️ Backend Agent")
            server_code = await st.write_stream(backend_agent_stream(ui_code, db_schema, st.session_state.be_memory))
            
            # STEP 4: QA LOOP
            max_retries = 2
            for attempt in range(max_retries):
                st.markdown(f"### 🕵️ QA Agent (Attempt {attempt+1})")
                qa_feedback = await st.write_stream(qa_agent_stream(server_code, st.session_state.qa_memory))
                
                if "PASS" in qa_feedback.upper():
                    st.success("✅ QA Passed! Code is ready.")
                    break
                else:
                    st.warning("⚠️ QA found issues. Backend is fixing...")
                    fix_prompt = f"The QA Agent found these issues. Please fix them and return ONLY the updated Python code:\n\n{qa_feedback}"
                    
                    st.markdown("### ⚙️ Backend Agent (Fixing)")
                    server_code = await st.write_stream(backend_agent_stream("Keep previous HTML", fix_prompt, st.session_state.be_memory))
            
            return server_code

        final_code = asyncio.run(run_workflow())
        st.session_state.chat_history.append({"role": "assistant", "content": final_code})