import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Powiedz mi 'cześć' po polsku i wyjaśnij w jednym zdaniu, co to jest agent AI."
)

print(response.text)