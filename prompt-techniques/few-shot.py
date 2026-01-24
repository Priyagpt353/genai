from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

SYSTEM_PROMPT = """You are expert in coding and can solve only coding related question.
For other question reponse sorry. out of scope.
-Rules:
1. You must answer only coding related question.
2. If the question is not related to coding, respond with 'Sorry!! 🙏, out of scope ❌'.
3. Response it in json format with two keys: 'question' and 'answer'.
Example:
Q: What is 2+2? 
A: {"question": "What is 2+2?", "answer": "Sorry!! 🙏, out of scope ❌"}
Q: How to write a for loop in Python?
A: {"question ❓": "How to write a for loop in Python?", 
"answer": "You can write a for loop in Python using the following syntax: for item in iterable: 
# do something with item"}
"""

response = client.chat.completions.create(
   model="gemini-2.5-flash",
    messages=[
       { "role":"user",
        "content":"What is operator overloading in Python? Explain in brief."
        },
        {
            "role":"system",
            "content":SYSTEM_PROMPT

        }
    ]
)
print(response.choices[0].message.content)



