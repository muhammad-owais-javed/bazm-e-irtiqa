from core.llm_client import async_ask_agent_stream

async def backend_agent_stream(frontend_code, db_schema, memory=None):
    system_prompt = """You are an expert Python Backend Developer. 
    Wrap the provided HTML and SQL schema into a Python Flask server.
    IMPORTANT: First, write your step-by-step plan inside <thinking> tags. 
    Then, output the Python code inside a markdown code block."""
    
    combined_prompt = f"Frontend HTML:\n{frontend_code}\n\nDatabase SQL:\n{db_schema}"
    return async_ask_agent_stream("Backend Agent", system_prompt, combined_prompt, memory)
