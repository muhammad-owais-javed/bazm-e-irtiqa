import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

client = OpenAI(base_url=OLLAMA_URL, api_key="bazm-e-irtiqa-local")

def ask_agent(agent_name, system_prompt, user_message):
    """Core function to send tasks to local AI."""
    
    print(f"\n🤖 [{agent_name}] is thinking...")
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7 # Controls creativity (0 = strict, 1 = highly creative)
    )
    
    reply = response.choices[0].message.content
    print(f"✅ [{agent_name}] completed the task.")
    return reply


# --- Define Our Agents ---

def frontend_agent(requirements):
    system_prompt = """You are an expert Frontend Web Developer. 
    Your job is to write clean, modern HTML and inline CSS based on the user's requirements.
    Return ONLY the HTML code, no explanations."""
    
    return ask_agent("Frontend Agent", system_prompt, requirements)

def backend_agent(frontend_code):
    system_prompt = """You are an expert Python Backend Developer. 
    Your job is to take the provided HTML code and wrap it in a fully functional Python Flask server.
    Return ONLY the Python code, no explanations."""
    
    return ask_agent("Backend Agent", system_prompt, frontend_code)

def main():
    print("\n🚀 Welcome to Bazm-e-Irtiqa Interactive Mode!")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    while True:
        # 1. Get dynamic input from the user
        print("\n" + "-"*50)
        task = input("📝 Enter a task for the agents (or type 'exit' to quit):\n> ")
        
        if task.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        if not task.strip():
            continue

        print(f"\n📋 Task received: {task}")
        
        # 2. Run the workflow
        ui_code = frontend_agent(task)
        server_code = backend_agent(ui_code)
        
        # 3. Print the result
        print("\n" + "="*50)
        print("🎉 FINAL COORDINATED OUTPUT 🎉")
        print("="*50)
        print(server_code)

if __name__ == "__main__":
    main()
