from core.llm_client import ask_agent

def frontend_agent(requirements):
    system_prompt = """You are an expert Frontend Web Developer. 
    Your job is to write clean, modern HTML and inline CSS based on the user's requirements.
    Return ONLY the HTML code, no explanations."""
    
    return ask_agent("Frontend Agent", system_prompt, requirements)
