import streamlit as st
import asyncio
from agents.frontend import frontend_agent
from agents.database import database_agent
from agents.backend import backend_agent
from agents.qa import qa_agent
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
        
        async def run_workflow():
            # --- STEP 1: PARALLEL EXECUTION ---
            status_text.info("🎨 Frontend & 🗄️ Database agents are working in parallel...")
            results = await asyncio.gather(
                frontend_agent(task, st.session_state.fe_memory),
                database_agent(task, st.session_state.db_memory)
            )
            
            # SAFE UNPACKING: First split the two agent results, then unpack their memory
            res_fe, res_db = results
            ui_code, st.session_state.fe_memory = res_fe
            db_schema, st.session_state.db_memory = res_db
            
            with st.expander("🔍 View Parallel Outputs (HTML & SQL)"):
                st.code(ui_code, language='html')
                st.code(db_schema, language='sql')

            # --- STEP 2: SEQUENTIAL EXECUTION ---
            status_text.info("⚙️ Backend Agent is building the server...")
            server_code, st.session_state.be_memory = await backend_agent(ui_code, db_schema, st.session_state.be_memory)
            
            # --- STEP 3: QA FEEDBACK LOOP ---
            status_text.info("🕵️ QA Agent is reviewing the code...")
            max_retries = 2 # Prevent infinite loops
            
            for attempt in range(max_retries):
                qa_feedback, st.session_state.qa_memory = await qa_agent(server_code, st.session_state.qa_memory)
                
                if "PASS" in qa_feedback.upper():
                    status_text.success("✅ QA Passed! Code is ready.")
                    break
                else:
                    status_text.warning(f"⚠️ QA found issues (Attempt {attempt+1}/{max_retries}). Backend is fixing...")
                    with st.expander(f"🔍 QA Feedback (Attempt {attempt+1})"):
                        st.write(qa_feedback)
                    
                    # Send the QA feedback back to the Backend Agent to fix!
                    fix_prompt = f"The QA Agent found these issues. Please fix them and return ONLY the updated Python code:\n\n{qa_feedback}"
                    server_code, st.session_state.be_memory = await backend_agent("Keep previous HTML", fix_prompt, st.session_state.be_memory)
            
            return server_code

        # Run the async workflow inside Streamlit
        final_code = asyncio.run(run_workflow())
        
        # Save and display final output
        st.session_state.chat_history.append({"role": "assistant", "content": f"```python\n{final_code}\n```"})
        st.code(final_code, language='python')
