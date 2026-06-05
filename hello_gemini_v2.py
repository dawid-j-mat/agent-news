import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

system_instruction = """Jesteś doswiadczonym redaktorem prasowki naukowej.
Tworzysz zwiezle, rzeczowe streszczenia tekstow naukowych po polsku.
Pisz proza, bez wypunktowan. Maksymalnie 3 zdania na streszczenie.
Nie dodawaj wstepow ani podsumowan typu 'Oto streszczenie:'."""

user_message = """Streszcz mi w trzech zdaniach, czym rozni sie 
uczenie nadzorowane od uczenia przez wzmacnianie w kontekscie 
trenowania duzych modeli jezykowych."""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        max_output_tokens=500,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    ),
    contents=user_message,
)

print(response.text)
print("\n---")
print(f"Tokeny wejscia: {response.usage_metadata.prompt_token_count}")
print(f"Tokeny wyjscia: {response.usage_metadata.candidates_token_count}")
print(f"Tokeny lacznie: {response.usage_metadata.total_token_count}")