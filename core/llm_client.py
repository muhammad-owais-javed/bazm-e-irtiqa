import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

aclient = AsyncOpenAI(base_url=OLLAMA_URL, api_key="bazm-e-irtiqa-local")

async def async_ask_agent(agent_name, system_prompt, user_message, memory=None):
    """Standard async function (No streaming)"""
    if memory is None:
        memory = [{"role": "system", "content": system_prompt}]
        
    memory.append({"role": "user", "content": user_message})
    
    response = await aclient.chat.completions.create(
        model=MODEL_NAME,
        messages=memory,
        temperature=0.7
    )
    
    reply = response.choices[0].message.content
    memory.append({"role": "assistant", "content": reply})
    return reply, memory

async def async_ask_agent_stream(agent_name, system_prompt, user_message, memory):
    """New Streaming function for the UI and CLI"""
    # If the memory list is empty, initialize it with the system prompt
    if len(memory) == 0:
        memory.append({"role": "system", "content": system_prompt})
        
    memory.append({"role": "user", "content": user_message})
    
    response = await aclient.chat.completions.create(
        model=MODEL_NAME,
        messages=memory,
        temperature=0.7,
        stream=True # Enable streaming
    )
    
    full_reply = ""
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_reply += content
            yield content # Yield chunk to the interface
            
    # Save the final combined reply to memory (No return statement needed!)
    memory.append({"role": "assistant", "content": full_reply})
