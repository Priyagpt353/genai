from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"user","content":"what is a+b"},
        {"role":"system","content":"You are a expert in coding with Python and "
        "can answer only question related to python programgin language. "
        "For other question reponse sorry"}
        ]
)

print(response.choices[0].message.content)

