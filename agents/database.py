from core.llm_client import async_ask_agent_stream

def database_agent_stream(requirements, memory=None):
    system_prompt = """You are an expert Database Architect. 
    Write the SQL schema based on the user's requirements.
    IMPORTANT: First, write your step-by-step plan inside <thinking> tags. 
    Then, output the SQL code inside a markdown code block."""
    
    return async_ask_agent_stream("Database Agent", system_prompt, requirements, memory)
