from core.llm_client import async_ask_agent

async def qa_agent(code_to_review, memory=None):
    system_prompt = """You are an expert Quality Assurance (QA) Engineer and Code Reviewer.
    Review the provided Python code for syntax errors, bugs, or missing imports.
    If the code is perfect, reply with exactly the word: PASS
    If there are errors, explain them clearly so the developer can fix them."""
    
    return await async_ask_agent("QA Agent", system_prompt, code_to_review, memory)
