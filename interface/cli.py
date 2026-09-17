import asyncio
from agents.frontend import frontend_agent
from agents.database import database_agent
from agents.backend import backend_agent
from agents.qa import qa_agent
from core.llm_client import MODEL_NAME

async def main():
    print("\n🚀 Welcome to Bazm-e-Irtiqa Interactive Mode (Parallel + QA + Memory)!")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    # Initialize empty memory for all four agents
    fe_memory, db_memory, be_memory, qa_memory = None, None, None, None
    
    while True:
        print("\n" + "-"*50)
        task = input("📝 Enter a task (or type 'exit'):\n> ")
        
        if task.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        if not task.strip():
            continue

        # --- STEP 1: PARALLEL EXECUTION ---
        print("\n🎨 Frontend & 🗄️ Database agents are working in parallel...")
        results = await asyncio.gather(
            frontend_agent(task, fe_memory),
            database_agent(task, db_memory)
        )
        
        # Safe unpacking
        res_fe, res_db = results
        ui_code, fe_memory = res_fe
        db_schema, db_memory = res_db
        
        # --- STEP 2: SEQUENTIAL EXECUTION ---
        print("⚙️ Backend Agent is building the server...")
        server_code, be_memory = await backend_agent(ui_code, db_schema, be_memory)
        
        # --- STEP 3: QA FEEDBACK LOOP ---
        print("🕵️ QA Agent is reviewing the code...")
        max_retries = 2
        
        for attempt in range(max_retries):
            qa_feedback, qa_memory = await qa_agent(server_code, qa_memory)
            
            if "PASS" in qa_feedback.upper():
                print("✅ QA Passed! Code is ready.")
                break
            else:
                print(f"⚠️ QA found issues (Attempt {attempt+1}/{max_retries}). Backend is fixing...")
                
                # Send the QA feedback back to the Backend Agent to fix!
                fix_prompt = f"The QA Agent found these issues. Please fix them and return ONLY the updated Python code:\n\n{qa_feedback}"
                server_code, be_memory = await backend_agent("Keep previous HTML", fix_prompt, be_memory)
        
        # --- FINAL OUTPUT ---
        print("\n" + "="*50)
        print("🎉 FINAL COORDINATED OUTPUT 🎉")
        print("="*50)
        print(server_code)

if __name__ == "__main__":
    asyncio.run(main())
