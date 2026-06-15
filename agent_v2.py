import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from narzedzie_v1 import podaj_dzisiejsza_date

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

config = types.GenerateContentConfig(
    tools=[podaj_dzisiejsza_date],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

odpowiedz = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Jaka jest dzisiaj data?",
    config=config,
)

print("=== Cala odpowiedz modelu (surowa) ===")
print(odpowiedz.candidates[0].content.parts[0])