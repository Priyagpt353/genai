from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")  # Use the correct variable name

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """You are expert in mathematics and answer only question related to 
mathematics. For other question reponse sorry."""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": "Explain to me how AI works in 2-3 lines"
        },
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]
)

print(response.choices[0].message.content)


