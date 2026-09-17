from agents.frontend import frontend_agent
from agents.backend import backend_agent
from core.llm_client import MODEL_NAME

def main():
    print("\n🚀 Welcome to Bazm-e-Irtiqa Interactive Mode!")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    while True:
        print("\n" + "-"*50)
        task = input("📝 Enter a task for the agents (or type 'exit' to quit):\n> ")
        
        if task.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        if not task.strip():
            continue

        print(f"\n📋 Task received: {task}")
        
        ui_code = frontend_agent(task)
        server_code = backend_agent(ui_code)
        
        print("\n" + "="*50)
        print("🎉 FINAL COORDINATED OUTPUT 🎉")
        print("="*50)
        print(server_code)

if __name__ == "__main__":
    main()
