from core.llm_client import async_ask_agent

async def backend_agent(frontend_code, db_schema, memory=None):
    system_prompt = """You are an expert Python Backend Developer. 
    Wrap the provided HTML and SQL schema into a Python Flask server.
    Return ONLY the Python code."""
    
    # Combine both parallel outputs into one prompt for the backend
    combined_prompt = f"Frontend HTML:\n{frontend_code}\n\nDatabase SQL:\n{db_schema}"
    
    return await async_ask_agent("Backend Agent", system_prompt, combined_prompt, memory)
