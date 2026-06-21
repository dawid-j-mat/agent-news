import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from narzedzie_pobierz_v1 import pobierz_tekst_ze_strony

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

config = types.GenerateContentConfig(
    tools=[pobierz_tekst_ze_strony],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

dostepne_narzedzia = {
    "pobierz_tekst_ze_strony": pobierz_tekst_ze_strony,
}

historia = [
    types.Content(
        role="user",
        parts=[types.Part(text="Pobierz tekst ze strony https://example.com i powiedz mi w jednym zdaniu, czego dotyczy.")],
    )
]

MAKS_ITERACJI = 5
for numer_iteracji in range(MAKS_ITERACJI):
    print(f"--- Iteracja {numer_iteracji + 1} ---")

    odpowiedz = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=historia,
        config=config,
    )

    czesc = odpowiedz.candidates[0].content.parts[0]

    if czesc.function_call:
        nazwa = czesc.function_call.name
        argumenty = dict(czesc.function_call.args)
        print(f"Model prosi o narzedzie: {nazwa}, argumenty: {argumenty}")

        historia.append(odpowiedz.candidates[0].content)

        funkcja = dostepne_narzedzia[nazwa]
        wynik = funkcja(**argumenty)
        print(f"Wynik narzedzia (pierwsze 200 znakow): {wynik[:200]}")

        historia.append(
            types.Content(
                role="user",
                parts=[types.Part(
                    function_response=types.FunctionResponse(
                        name=nazwa,
                        response={"wynik": wynik},
                    )
                )],
            )
        )
    else:
        print("=== Odpowiedz koncowa ===")
        print(czesc.text)
        break