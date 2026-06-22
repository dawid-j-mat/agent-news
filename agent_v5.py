import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from narzedzie_rss_v1 import pobierz_naglowki_z_rss
from narzedzie_pobierz_v1 import pobierz_tekst_ze_strony

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

config = types.GenerateContentConfig(
    tools=[pobierz_naglowki_z_rss, pobierz_tekst_ze_strony],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

dostepne_narzedzia = {
    "pobierz_naglowki_z_rss": pobierz_naglowki_z_rss,
    "pobierz_tekst_ze_strony": pobierz_tekst_ze_strony,
}

historia = [
    types.Content(
        role="user",
        parts=[types.Part(text=(
            "Sprawdz kanal RSS https://deepmind.google/blog/rss.xml "
            "i znajdz na liscie wpis o bezpieczenstwie agentow AI "
            "('Securing the future of AI agents'). Pobierz jego pelna "
            "tresc i streszcz ja po polsku w trzech zdaniach."
        ))],
    )
]

MAKS_ITERACJI = 10
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
        print(f"Wynik narzedzia (pierwsze 200 znakow): {str(wynik)[:200]}")

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