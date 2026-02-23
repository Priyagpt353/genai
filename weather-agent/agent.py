from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
weather_key = os.getenv("WEATHER_API_KEY")

client = OpenAI(  
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

def get_weather_info(location):
    url =f"https://api.weatherapi.com/v1/current.json?key={weather_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current = data.get("current", {})
        location = current.get("condition", {}).get("text", "Unknown location")
        temp_c = current.get("temp_c")
        return f"The current weather in {location} is {temp_c}°C, {location}"
    else:
        return {"error": f"Failed to fetch weather: {response.status_code}"}

SYSTEM_PROMPT = """ You are expert AI assitant in resolving user queries step by step using chain 
of thought prompting. 
Your name is Loki and you are very helpful and intelligent.
You task is to break down the complex problems into smaller steps to arrive at the final answer.
You work on START, PLAN and OUPUT steps.
First you need to PLAN how to get the solve the problem step by step.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
You can also call a tool if required from the list of available tools.
for every tool call wait for the observe step which is the output from the called tool.

    -Rules:
    1. You must answer step by step.
    2. Explain each step clearly before moving to the next step.
    3. Finally provide the final answer after all the steps.
    4. The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and 
        finally OUTPUT (which is going to the displayed to the user).

      PLAN (That can be multiple times) and finally 
      OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", 
        "input": "string" }

    Available Tools:
    - get_weather(location: str): Takes city name as an input string and returns the 
        weather info about the city.

     Example:
     Q: What is the sum of first 10 natural numbers?
     A: 
     START: { "step": "START", 
            "content": "Tell me the current real time temperature in Gorakhpur in C" }
     PLAN: { "step": "PLAN", 
            "content": "Seems like user is interested in knowing the current temperature 
            in Gorakhpur." }
     PLAN: { "step": "PLAN", 
            "content": "Let's see we have any tools to get the weather information." }
     TOOL: { "step": "TOOL", 
            "content": "Calling get_weather with input 'Gorakhpur'", 
            "tool": "get_weather", 
            "input": "Gorakhpur" }
     PLAN: { "step": "PLAN", 
            "content": "Great, I got the weather info about Gorakhpur" }
     OUTPUT: { "step": "OUTPUT", 
                "content": "The current weather in Gorakhpur is 25°C, Sunny." }
"""
    
available_tools = {
    "get_weather": get_weather_info
}

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
        elif step == "TOOL":
            print("🔧", content)
        elif step == "OUTPUT":
            print("🤖", content)
            break

    if any(r.get("step") == "OUTPUT" for r in results):
        break

