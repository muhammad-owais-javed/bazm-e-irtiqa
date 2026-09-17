from core.llm_client import async_ask_agent

async def database_agent(requirements, memory=None):
    system_prompt = """You are an expert Database Architect. 
    Write the SQL schema based on the user's requirements.
    Return ONLY the SQL code, no explanations."""
    
    return await async_ask_agent("Database Agent", system_prompt, requirements, memory)
