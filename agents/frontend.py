from core.llm_client import async_ask_agent_stream

async def frontend_agent_stream(requirements, memory=None):
    system_prompt = """You are an expert Frontend Web Developer. 
    Write clean HTML/CSS based on the requirements. 
    IMPORTANT: First, write your step-by-step plan inside <thinking> tags. 
    Then, output the HTML code inside a markdown code block."""
    
    return async_ask_agent_stream("Frontend Agent", system_prompt, requirements, memory)
