from google import genai

client = genai.Client(api_key="AIzaSyA1MTB2L09d-Yf6JnF09ddSpniMhLaUIp4")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)