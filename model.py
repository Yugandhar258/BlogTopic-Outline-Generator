import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

def get_llm(temperature: float = 0.7):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Please add it to your .env file."
        )
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=api_key,
    )
    return llm

def call_llm(prompt_text: str, temperature: float = 0.7) -> str:
    llm = get_llm(temperature=temperature)
    messages = [HumanMessage(content=prompt_text)]
    response = llm.invoke(messages)
    return response.content