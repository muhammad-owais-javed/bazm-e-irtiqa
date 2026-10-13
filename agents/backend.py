from core.llm_client import async_ask_agent_stream

def backend_agent_stream(frontend_code, db_schema, memory=None):
    system_prompt = """You are an expert Python Backend Developer. 
    Wrap the provided HTML and SQL schema into a Python Flask server.
    IMPORTANT RULES:
    1. First, write your step-by-step plan inside <thinking> tags. 
    2. Output the Python code inside a markdown code block.
    3. You MUST serve the HTML on the root route ('/').
    4. You MUST run the app on port 5000 using exactly: app.run(host='0.0.0.0', port=5000)"""
    
    combined_prompt = f"Frontend HTML:\n{frontend_code}\n\nDatabase SQL:\n{db_schema}"
    return async_ask_agent_stream("Backend Agent", system_prompt, combined_prompt, memory)
