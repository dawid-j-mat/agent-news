import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_GLOWNY = "gemini-3.8-flash"
MODEL_ZAPASOWY = "gemini-3.5-flash-lite"

KODY_CHWILOWE = {429, 500, 503}
LICZBA_PROB = 4


def zapytaj_model(tresc, config, modele=(MODEL_GLOWNY, MODEL_ZAPASOWY)):
    """Wysyla zapytanie do modelu i zwraca jego odpowiedz.

    Przy chwilowych bledach (przeciazenie, limit) ponawia probe z coraz
    dluzsza przerwa. Gdy model glowny nie odpowie, przechodzi na zapasowy.
    Gdy zaden nie odpowie, zwraca None.
    """
    for model in modele:
        for proba in range(1, LICZBA_PROB + 1):
            try:
                return client.models.generate_content(
                    model=model,
                    contents=tresc,
                    config=config,
                )
            except errors.APIError as blad:
                print(f"   [{model}] proba {proba}: BLAD {blad.code}: {blad.message}")
                if blad.code not in KODY_CHWILOWE or proba == LICZBA_PROB:
                    break
                przerwa = 5 * 2 ** (proba - 1)
                print(f"   ...czekam {przerwa} s")
                time.sleep(przerwa)
        print(f"   Model {model} nie odpowiedzial.")
    return None


if __name__ == "__main__":
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
        max_output_tokens=2000,
    )
    pytanie = (
        "Wyjasnij w trzech prostych zdaniach, czym jest model jezykowy "
        "o otwartych wagach. Pisz dla osoby bez wyksztalcenia informatycznego."
    )

    start = time.time()
    odpowiedz = zapytaj_model(pytanie, config)
    czas = time.time() - start

    if odpowiedz is None:
        print("Zaden model nie odpowiedzial.")
    else:
        print(f"\nOdpowiedzial: {odpowiedz.model_version} (lacznie {czas:.1f} s)\n")
        print(odpowiedz.text)
        u = odpowiedz.usage_metadata
        print(
            f"--- wejscie: {u.prompt_token_count}"
            f" | myslenie: {u.thoughts_token_count}"
            f" | odpowiedz: {u.candidates_token_count}"
        )