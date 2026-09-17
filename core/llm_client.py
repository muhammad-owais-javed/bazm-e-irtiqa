import os
from dotenv import load_dotenv
from openai import OpenAI

# Load configuration
load_dotenv()
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

# Initialize client
client = OpenAI(base_url=OLLAMA_URL, api_key="bazm-e-irtiqa-local")

def ask_agent(agent_name, system_prompt, user_message):
    """Core function to send tasks to our local AI."""
    
    print(f"\n🤖 [{agent_name}] is thinking...")
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    reply = response.choices[0].message.content
    print(f"✅ [{agent_name}] completed the task.")
    return reply
