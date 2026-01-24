from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyA1MTB2L09d-Yf6JnF09ddSpniMhLaUIp4",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "user",
            "content": "Explain to me how AI works in 2-3 lines"
        }
    ]
)

print(response.choices[0].message.content)