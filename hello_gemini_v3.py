import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

system_instruction = "Jestes pomocnym asystentem. Odpowiadasz zwiezle, po polsku."

# Historia rozmowy — lista wiadomosci. Na poczatku pusta.
historia = []

# --- TURA 1 ---
historia.append(
    types.Content(role="user", parts=[types.Part(text="Mam na imie Dawid.")])
)

odpowiedz1 = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    ),
    contents=historia,
)

print("MODEL:", odpowiedz1.text)

# Dopisujemy odpowiedz modelu do historii.
historia.append(
    types.Content(role="model", parts=[types.Part(text=odpowiedz1.text)])
)

# --- TURA 2 ---
historia.append(
    types.Content(role="user", parts=[types.Part(text="Jak mam na imie?")])
)

odpowiedz2 = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    ),
    contents=historia,
)

print("MODEL:", odpowiedz2.text)