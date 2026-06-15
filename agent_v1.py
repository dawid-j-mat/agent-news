import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from narzedzie_v1 import podaj_dzisiejsza_date

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

config = types.GenerateContentConfig(
    tools=[podaj_dzisiejsza_date],
)

odpowiedz = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Jaka jest dzisiaj data?",
    config=config,
)

print(odpowiedz.text)