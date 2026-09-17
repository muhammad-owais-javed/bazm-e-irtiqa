from core.llm_client import async_ask_agent

async def frontend_agent(requirements, memory=None):
    system_prompt = """You are an expert Frontend Web Developer. 
    Write clean HTML/CSS based on the requirements. Return ONLY HTML."""
    
    return await async_ask_agent("Frontend Agent", system_prompt, requirements, memory)
