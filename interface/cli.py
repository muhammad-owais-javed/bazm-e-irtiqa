import asyncio
from agents.frontend import frontend_agent
from agents.database import database_agent
from agents.backend import backend_agent
from core.llm_client import MODEL_NAME

async def main():
    print("\n🚀 Welcome to Bazm-e-Irtiqa Interactive Mode (Parallel + Memory)!")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    # Initialize empty memory for all three agents
    fe_memory, db_memory, be_memory = None, None, None
    
    while True:
        print("\n" + "-"*50)
        task = input("📝 Enter a task (or type 'exit'):\n> ")
        
        if task.lower() in ['exit', 'quit']:
            break
        if not task.strip():
            continue

        # --- PARALLEL EXECUTION ---
        # Both agents work at the exact same time!
        results = await asyncio.gather(
            frontend_agent(task, fe_memory),
            database_agent(task, db_memory)
        )
        
        # Unpack the results and update their memories
        (ui_code, fe_memory), (db_schema, db_memory) = results
        
        # --- SEQUENTIAL EXECUTION ---
        # Backend waits for the parallel tasks to finish, then does its job
        server_code, be_memory = await backend_agent(ui_code, db_schema, be_memory)
        
        print("\n" + "="*50)
        print("🎉 FINAL COORDINATED OUTPUT 🎉")
        print("="*50)
        print(server_code)

if __name__ == "__main__":
    # Run the async event loop
    asyncio.run(main())
