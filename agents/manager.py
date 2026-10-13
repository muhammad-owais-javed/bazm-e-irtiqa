from core.llm_client import async_ask_agent_stream

async def manager_agent(user_prompt, memory=None):
    """Decides if this is a web app, a simple script, or just a chat."""
    system_prompt = """You are the Manager Agent. Read the user's prompt.
    Reply with EXACTLY ONE of these three words:
    WEB_APP - If they want a full web application with a server/UI.
    SCRIPT - If they want a simple Python script or calculation.
    CHAT - If they are just asking a question or talking.
    Do NOT include <thinking> tags or any other text. Just the single word."""
    
    # We don't stream this one because it's just a routing decision in the background
    from core.llm_client import async_ask_agent
    reply, _ = await async_ask_agent("Manager", system_prompt, user_prompt, memory)
    
    # Clean the response to ensure it matches our keywords
    reply = reply.strip().upper()
    if "WEB_APP" in reply: return "WEB_APP"
    if "SCRIPT" in reply: return "SCRIPT"
    return "CHAT"
