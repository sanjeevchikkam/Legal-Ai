import os
from langchain_cerebras import ChatCerebras


_client = ChatCerebras(
    api_key=os.getenv("CEREBRAS_API_KEY"),
    model="llama3.1-8b",
    temperature=0.2,
    max_tokens=1500,
)


def call_llm(system_prompt: str, user_message: str) -> str:
    """
    Sends the assembled prompt to Cerebras LLM.
    Returns the assistant's reply as a plain string.
    """
    messages = [
        ("system", system_prompt),
        ("human",  user_message),
    ]
    response = _client.invoke(messages)
    return response.content.strip()