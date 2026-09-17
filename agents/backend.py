from core.llm_client import ask_agent

def backend_agent(frontend_code):
    system_prompt = """You are an expert Python Backend Developer. 
    Your job is to take the provided HTML code and wrap it in a fully functional Python Flask server.
    Return ONLY the Python code, no explanations."""
    
    return ask_agent("Backend Agent", system_prompt, frontend_code)
