from agents.frontend import frontend_agent
from agents.backend import backend_agent
from core.llm_client import MODEL_NAME

def main():
    print("🚀 Starting Bazm-e-Irtiqa Ping Test...")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    task = "Create a beautiful 'Hello World' landing page with a dark mode theme."
    print(f"\n📋 Task: {task}")
    
    ui_code = frontend_agent(task)
    server_code = backend_agent(ui_code)
    
    print("\n" + "="*50)
    print("🎉 FINAL COORDINATED OUTPUT 🎉")
    print("="*50)
    print(server_code)

if __name__ == "__main__":
    main()
