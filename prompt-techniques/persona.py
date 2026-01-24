from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

SYSTEM_PROMPT = """You are a Priya Gupta an 28years old tech girl.
Who is exploring AI models and building projects.
Your main tech stack is JS and Python and You are leaning GenAI these days."""

response = client.chat.completions.create(
   model="gemini-2.5-flash",
    messages=[
       { "role":"user",
        "content":"Hey there! Can you tell me about yourself?"
        },
        {
            "role":"system",
            "content":SYSTEM_PROMPT

        }
    ]
)
print(response.choices[0].message.content)



