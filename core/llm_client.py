import os
from dotenv import load_dotenv
from openai import AsyncOpenAI # Notice the Async client!

# Load configuration
load_dotenv()
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

# Initialize client
aclient = AsyncOpenAI(base_url=OLLAMA_URL, api_key="bazm-e-irtiqa-local")

async def async_ask_agent_stream(agent_name, system_prompt, user_message, memory):
    """Core async function that supports conversation memory."""
    
    print(f"\n🤖 [{agent_name}] is thinking...")
    
    """Streams the response chunk by chunk."""
    if not memory:
        memory.extend([{"role": "system", "content": system_prompt}])
        
    # Add the new user message to the memory
    memory.append({"role": "user", "content": user_message})
    
    
    response = await aclient.chat.completions.create(
        model=MODEL_NAME,
        messages=memory,
        temperature=0.7,
        stream=True # Enable streaming!
    )
    
    full_reply = ""
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_reply += content
            yield content # Send the chunk to the UI immediately
            
    
    # Add the AI's reply to the memory so it remembers it for next time
    memory.append({"role": "assistant", "content": full_reply})

    print(f"✅ [{agent_name}] completed the task.")
    return full_reply, memory
