import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODELE = ["gemini-3.8-flash", "gemini-3.5-flash-lite"]

PYTANIE = (
    "Wyjasnij w trzech prostych zdaniach, czym jest model jezykowy "
    "o otwartych wagach. Pisz dla osoby bez wyksztalcenia informatycznego."
)

config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level="low"),
    max_output_tokens=2000,
)

for model in MODELE:
    print(f"\n=== {model} ===")
    start = time.time()
    try:
        odpowiedz = client.models.generate_content(
            model=model,
            contents=PYTANIE,
            config=config,
        )
    except errors.APIError as blad:
        print(f"BLAD {blad.code}: {blad.message}")
        continue
    czas = time.time() - start

    print(odpowiedz.text)
    u = odpowiedz.usage_metadata
    print(
        f"--- czas: {czas:.1f} s | wejscie: {u.prompt_token_count}"
        f" | myslenie: {u.thoughts_token_count}"
        f" | odpowiedz: {u.candidates_token_count}"
        f" | lacznie: {u.total_token_count}"
    )