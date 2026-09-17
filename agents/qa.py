from core.llm_client import async_ask_agent_stream

async def qa_agent_stream(code_to_review, memory=None):
    system_prompt = """You are an expert Quality Assurance (QA) Engineer.
    Review the provided Python code for syntax errors or bugs.
    IMPORTANT: First, write your step-by-step plan inside <thinking> tags. 
    If the code is perfect, end your response with exactly the word: PASS
    If there are errors, explain them clearly so the developer can fix them."""
    
    return async_ask_agent_stream("QA Agent", system_prompt, code_to_review, memory)
