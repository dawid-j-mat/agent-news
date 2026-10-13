import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

DOSTAWCY = {
    "ovh": {
        "adres": "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1",
        "model": "Qwen3.5-397B-A17B",
        "klucz": None,
    },
    "nvidia": {
        "adres": "https://integrate.api.nvidia.com/v1",
        "model": "z-ai/glm-5.2",
        "klucz": os.getenv("NVIDIA_API_KEY"),
    },
}

WYBRANY = "ovh"

dostawca = DOSTAWCY[WYBRANY]

PYTANIE = (
    "Wyjasnij w trzech prostych zdaniach, czym jest model jezykowy "
    "o otwartych wagach. Pisz dla osoby bez wyksztalcenia informatycznego."
)

naglowki = {}
if dostawca["klucz"]:
    naglowki["Authorization"] = f"Bearer {dostawca['klucz']}"

zapytanie = {
    "model": dostawca["model"],
    "messages": [
        {"role": "user", "content": PYTANIE},
    ],
    "max_tokens": 4000,
}

print(f"=== {WYBRANY}: {dostawca['model']} ===")
start = time.time()
try:
    odpowiedz = requests.post(
        f"{dostawca['adres']}/chat/completions",
        headers=naglowki,
        json=zapytanie,
        timeout=120,
    )
    odpowiedz.raise_for_status()
except requests.exceptions.RequestException as blad:
    print("BLAD:", blad)
    if blad.response is not None:
        print(blad.response.text[:500])
    raise SystemExit
czas = time.time() - start

dane = odpowiedz.json()

print("\n--- surowa odpowiedz (poczatek) ---")
print(json.dumps(dane, indent=2, ensure_ascii=False)[:1500])

print("\n--- sama tresc ---")
print(dane["choices"][0]["message"]["content"])

zuzycie = dane.get("usage", {})
print(
    f"\n--- czas: {czas:.1f} s"
    f" | wejscie: {zuzycie.get('prompt_tokens')}"
    f" | wyjscie: {zuzycie.get('completion_tokens')}"
)