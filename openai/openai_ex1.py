from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role":"user","content":"Hey there!"}
    ]
)
print(response.choices[0].message.content)