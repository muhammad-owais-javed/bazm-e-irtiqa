import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load configuration from the .env file
load_dotenv()

# Default to 'phi3' if the .env file is missing
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 

#Get the URL from the environment, or default to localhost if running manually
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

# 2. Connect to local Dockerized AI Engine
client = OpenAI(
    base_url=OLLAMA_URL,
    api_key="bazm-e-irtiqa-local" # The library requires a key, but Ollama ignores it!
 )

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

# --- The Orchestrator ---

def main():
    print("🚀 Starting Bazm-e-Irtiqa Multiagent Workflow...")
    print(f"📦 Using Model: {MODEL_NAME}")
    
    # The initial task from the user
    task = "Create a beautiful 'Hello World' landing page with a dark mode theme."
    print(f"\n📋 Task: {task}")
    
    # Step 1: Orchestrator assigns task to Frontend Agent
    ui_code = frontend_agent(task)
    
    # Step 2: Orchestrator passes Frontend's output to Backend Agent
    server_code = backend_agent(ui_code)
    
    # Step 3: Final Output
    print("\n" + "="*50)
    print("🎉 FINAL COORDINATED OUTPUT 🎉")
    print("="*50)
    print(server_code)

if __name__ == "__main__":
    main()
