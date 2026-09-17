import os
from dotenv import load_dotenv
from openai import AsyncOpenAI # Notice the Async client!

# Load configuration
load_dotenv()
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

# Initialize client
aclient = AsyncOpenAI(base_url=OLLAMA_URL, api_key="bazm-e-irtiqa-local")

async def async_ask_agent(agent_name, system_prompt, user_message, memory=None):
    """Core async function that supports conversation memory."""
    
    print(f"\n🤖 [{agent_name}] is thinking...")
    
    # If this is the first message, initialize the memory with the system prompt
    if memory is None:
        memory = [{"role": "system", "content": system_prompt}]
        
    # Add the new user message to the memory
    memory.append({"role": "user", "content": user_message})
    
    
    response = await aclient.chat.completions.create(
        model=MODEL_NAME,
        messages=memory,
        temperature=0.7
    )
    
    reply = response.choices[0].message.content
    
    # Add the AI's reply to the memory so it remembers it for next time
    memory.append({"role": "assistant", "content": reply})

    print(f"✅ [{agent_name}] completed the task.")
    return reply, memory
