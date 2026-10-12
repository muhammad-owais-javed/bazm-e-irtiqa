import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from core.metrics import start_agent_metrics_server, record_usage, track_latency, track_stream_latency


load_dotenv()
MODEL_NAME = os.getenv("LLM_MODEL", "phi3") 
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1" )

aclient = AsyncOpenAI(base_url=OLLAMA_URL, api_key="bazm-e-irtiqa-local")

start_agent_metrics_server()

@track_latency

async def async_ask_agent(agent_name, system_prompt, user_message, memory=None):
    """Standard async function (No streaming)"""
    if memory is None:
        memory = [{"role": "system", "content": system_prompt}]
        
    memory.append({"role": "user", "content": user_message})
    
    response = await aclient.chat.completions.create(
        model=MODEL_NAME,
        messages=memory,
        temperature=0.2
    )
    
    # Record tokens
    if response.usage:
        record_usage(
            agent_name, 
            response.usage.prompt_tokens, 
            response.usage.completion_tokens
        )
        
        
    reply = response.choices[0].message.content
    memory.append({"role": "assistant", "content": reply})
    return reply, memory

@track_stream_latency

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
        
    # Record stream tokens
        if hasattr(chunk, 'usage') and chunk.usage is not None:
            record_usage(
                agent_name,
                chunk.usage.prompt_tokens,
                chunk.usage.completion_tokens
            )
            
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_reply += content
            yield content # Yield chunk to the interface
            
    # Save the final combined reply to memory (No return statement needed)
    memory.append({"role": "assistant", "content": full_reply})
