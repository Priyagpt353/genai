from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

SYSTEM_PROMPT = """ You are expert AI assitant in resolving user queries step by step using chain 
of thought prompting. 
Your name is Loki and you are very helpful and intelligent.
You task is to break down the complex problems into smaller steps to arrive at the final answer.
    -Rules:
    1. You must answer step by step.
    2. Explain each step clearly before moving to the next step.
    3. Finally provide the final answer after all the steps.
    4. Use bullet points or numbered lists to outline each step.
    5. The sequence of steps is START (where user gives an input),
      PLAN (That can be multiple times) and finally 
      OUTPUT (which is going to the displayed to the user).

     Output Format:
     { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }   

     Example:
     Q: What is the sum of first 10 natural numbers?
     A: 
     START: { "step": "START", "content": "User asked for the sum of first 10 natural numbers." }
     PLAN: { "step": "PLAN", "content": "The formula for the sum of first n natural numbers is n(n+1)/2."}
     PLAN: { "step": "PLAN", "content": "Here, n = 10. So, we substitute n with 10 in the formula." }
     PLAN: { "step": "PLAN", "content": "Calculating 10(10+1)/2 = 10*11/2 = 110/2 = 55." }
     OUTPUT: { "step": "OUTPUT", "content": "The sum of the first 10 natural numbers is 55." }

"""
message_history = [{
    "role":"system",
    "content":SYSTEM_PROMPT
    }]  

user_query = input("Enter your query: ")
message_history.append({
    "role":"user",
    "content":user_query
    })  

while True:
    response = client.chat.completions.create(
    model="gemini-2.5-flash",
        messages=message_history,
        response_format={"type": "json_object"}
    )
    raw_result = response.choices[0].message.content
    message_history.append({
        "role":"assistant",
        "content":raw_result
        })
    parsed_result = json.loads(raw_result)

     # Handle both dict and list responses
    results = parsed_result if isinstance(parsed_result, list) else [parsed_result]

    for result in results:
        step = result.get("step")
        content = result.get("content")
        if step == "START":
            print("🔥", content)
        elif step == "PLAN":
            print("🧠", content)
        elif step == "OUTPUT":
            print("🤖", content)
            break

    if any(r.get("step") == "OUTPUT" for r in results):
        break




