import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from narzedzie_v1 import podaj_dzisiejsza_date

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Slownik: nazwa narzedzia -> faktyczna funkcja Pythona
dostepne_narzedzia = {
    "podaj_dzisiejsza_date": podaj_dzisiejsza_date,
}

config = types.GenerateContentConfig(
    tools=[podaj_dzisiejsza_date],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

# Historia rozmowy - ta sama lista co w Fazie 2
historia = [
    types.Content(
        role="user",
        parts=[types.Part(text="Jaka jest dzisiaj data?")],
    )
]

# --- PETLA AGENTOWA ---
MAKS_ITERACJI = 5
for numer_iteracji in range(MAKS_ITERACJI):
    print(f"--- Iteracja {numer_iteracji + 1} ---")

    odpowiedz = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=historia,
        config=config,
    )

    czesc = odpowiedz.candidates[0].content.parts[0]

    # Czy model prosi o narzedzie?
    if czesc.function_call:
        nazwa = czesc.function_call.name
        argumenty = dict(czesc.function_call.args)
        print(f"Model prosi o narzedzie: {nazwa}, argumenty: {argumenty}")

        # Dopisujemy prosbe modelu do historii
        historia.append(odpowiedz.candidates[0].content)

        # Wykonujemy wlasciwe narzedzie
        funkcja = dostepne_narzedzia[nazwa]
        wynik = funkcja(**argumenty)
        print(f"Wynik narzedzia: {wynik}")

        # Dopisujemy wynik do historii jako osobna wiadomosc
        historia.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=nazwa,
                            response={"wynik": wynik},
                        )
                    )
                ],
            )
        )
    else:
        # Model zwrocil zwykly tekst - koniec pracy
        print("=== Odpowiedz koncowa ===")
        print(czesc.text)
        break