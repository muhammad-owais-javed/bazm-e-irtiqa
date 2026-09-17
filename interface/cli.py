import asyncio
import sys
from agents.frontend import frontend_agent_stream
from agents.database import database_agent_stream
from agents.backend import backend_agent_stream
from agents.qa import qa_agent_stream
from core.llm_client import MODEL_NAME

async def stream_to_console(generator):
    """Helper function to print the stream to the terminal like a typewriter."""
    full_text = ""
    async for chunk in generator:
        sys.stdout.write(chunk)
        sys.stdout.flush()
        full_text += chunk
    print("\n") # Add a newline when finished
    return full_text

async def main():
    print("\n🚀 Welcome to Bazm-e-Irtiqa Interactive Mode (Streaming + QA)!")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    # IMPORTANT: Initialize memory as empty lists so they can be updated in-place!
    fe_memory, db_memory, be_memory, qa_memory = [], [], [], []
    
    while True:
        print("-" * 50)
        task = input("📝 Enter a task (or type 'exit'):\n> ")
        
        if task.lower() in ['exit', 'quit']:
            break
        if not task.strip():
            continue

        # --- SEQUENTIAL STREAMING ---
        # We run them sequentially in the CLI so the text doesn't overlap on the screen
        print("\n### 🎨 Frontend Agent")
        ui_code = await stream_to_console(frontend_agent_stream(task, fe_memory))
        
        print("### 🗄️ Database Agent")
        db_schema = await stream_to_console(database_agent_stream(task, db_memory))
        
        print("### ⚙️ Backend Agent")
        server_code = await stream_to_console(backend_agent_stream(ui_code, db_schema, be_memory))
        
        # --- QA LOOP ---
        max_retries = 2
        for attempt in range(max_retries):
            print(f"### 🕵️ QA Agent (Attempt {attempt+1})")
            qa_feedback = await stream_to_console(qa_agent_stream(server_code, qa_memory))
            
            if "PASS" in qa_feedback.upper():
                print("✅ QA Passed! Code is ready.\n")
                break
            else:
                print("⚠️ QA found issues. Backend is fixing...\n")
                fix_prompt = f"The QA Agent found these issues. Please fix them and return ONLY the updated Python code:\n\n{qa_feedback}"
                
                print("### ⚙️ Backend Agent (Fixing)")
                server_code = await stream_to_console(backend_agent_stream("Keep previous HTML", fix_prompt, be_memory))

if __name__ == "__main__":
    asyncio.run(main())
