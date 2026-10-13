import os
import time
import unicodedata
import requests
from dotenv import load_dotenv

load_dotenv()

DOSTAWCY = {
    "gemini": {
        "adres": "https://generativelanguage.googleapis.com/v1beta/openai",
        "klucz": os.getenv("GOOGLE_API_KEY"),
    },
    "ovh": {
        "adres": "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1",
        "klucz": None,
    },
    "nvidia": {
        "adres": "https://integrate.api.nvidia.com/v1",
        "klucz": os.getenv("NVIDIA_API_KEY"),
    },
}

KANDYDACI = [
    {"dostawca": "gemini", "model": "gemini-3.8-flash", "dodatki": {"reasoning_effort": "low"}},
    {"dostawca": "gemini", "model": "gemini-3.6-flash", "dodatki": {"reasoning_effort": "low"}},
    {"dostawca": "ovh", "model": "Qwen3.5-397B-A17B", "dodatki": {}},
    {"dostawca": "nvidia", "model": "z-ai/glm-5.3", "dodatki": {}},
    {"dostawca": "gemini", "model": "gemini-3.5-flash-lite", "dodatki": {"reasoning_effort": "low"}},
]

KODY_CHWILOWE = {429, 500, 502, 503, 504}
LICZBA_PROB = 4
LIMIT_CZASU_S = 90


def obce_znaki(tekst):
    """Zwraca zbior liter spoza alfabetu lacinskiego (np. hebrajskich, cyrylicy)."""
    return {
        znak for znak in tekst
        if znak.isalpha() and "LATIN" not in unicodedata.name(znak, "")
    }


def zapytaj_raz(kandydat, wiadomosci, max_tokenow):
    """Wysyla jedno zapytanie do jednego modelu i zwraca odpowiedz jako slownik."""
    dostawca = DOSTAWCY[kandydat["dostawca"]]

    naglowki = {}
    if dostawca["klucz"]:
        naglowki["Authorization"] = f"Bearer {dostawca['klucz']}"

    zapytanie = {
        "model": kandydat["model"],
        "messages": wiadomosci,
        "max_tokens": max_tokenow,
        **kandydat["dodatki"],
    }

    odpowiedz = requests.post(
        f"{dostawca['adres']}/chat/completions",
        headers=naglowki,
        json=zapytanie,
        timeout=LIMIT_CZASU_S,
    )
    odpowiedz.raise_for_status()
    dane = odpowiedz.json()

    wybor = dane["choices"][0]
    return {
        "tekst": (wybor["message"].get("content") or "").strip(),
        "powod_konca": wybor.get("finish_reason"),
        "dostawca": kandydat["dostawca"],
        "model": kandydat["model"],
        "zuzycie": dane.get("usage", {}),
    }


def zapytaj_model(wiadomosci, kandydaci=KANDYDACI, max_tokenow=8000):
    """Pyta kolejnych kandydatow, az ktorys da uzyteczna odpowiedz.

    Przy chwilowych bledach ponawia probe z coraz dluzsza przerwa. Przy
    bledach trwalych od razu przechodzi do nastepnego kandydata. Odrzuca
    odpowiedzi puste i zawierajace litery spoza alfabetu lacinskiego.
    Gdy zaden kandydat nie odpowie, zwraca None.
    """
    for kandydat in kandydaci:
        etykieta = f"{kandydat['dostawca']}/{kandydat['model']}"
        for proba in range(1, LICZBA_PROB + 1):
            try:
                wynik = zapytaj_raz(kandydat, wiadomosci, max_tokenow)
            except requests.exceptions.HTTPError as blad:
                kod = blad.response.status_code
                print(f"   [{etykieta}] proba {proba}: BLAD {kod}: {blad.response.text[:150]}")
                chwilowy = kod in KODY_CHWILOWE
            except requests.exceptions.RequestException as blad:
                print(f"   [{etykieta}] proba {proba}: problem z polaczeniem ({type(blad).__name__})")
                chwilowy = True
            else:
                if not wynik["tekst"]:
                    print(f"   [{etykieta}] proba {proba}: pusta odpowiedz (powod konca: {wynik['powod_konca']})")
                    chwilowy = False
                elif obce_znaki(wynik["tekst"]):
                    print(f"   [{etykieta}] proba {proba}: obce znaki w tekscie: {obce_znaki(wynik['tekst'])}")
                    chwilowy = True
                else:
                    return wynik

            if not chwilowy or proba == LICZBA_PROB:
                break
            przerwa = 5 * 2 ** (proba - 1)
            print(f"   ...czekam {przerwa} s")
            time.sleep(przerwa)
        print(f"   {etykieta} nie dal uzytecznej odpowiedzi.")
    return None


if __name__ == "__main__":
    TEKST_TESTOWY = (
        "TEST TEXT - fictional institution, used only to check summaries.\n"
        "Example University's library has finished a four-month pilot of an AI "
        "assistant that helps students search the catalogue. The assistant runs "
        "on an open-weight language model hosted on the university's own servers. "
        "340 students took part between March and June. Librarians reviewed a "
        "sample of 500 answers and judged 71 percent of them accurate; the most "
        "common error was citing call numbers that do not exist. The university "
        "has not yet decided whether to keep the tool after the pilot."
    )

    wiadomosci = [
        {
            "role": "system",
            "content": (
                "Jestes redaktorem prasowki dla dyrektora uczelni, ktory nie ma "
                "wyksztalcenia informatycznego. Streszczasz teksty po polsku, prosto "
                "i rzeczowo. Opierasz sie wylacznie na tresci tekstu: nie dopisujesz "
                "faktow, liczb, zalet ani wnioskow, ktorych w nim nie ma."
            ),
        },
        {
            "role": "user",
            "content": "Strescz ten tekst w trzech zdaniach.\n\n" + TEKST_TESTOWY,
        },
    ]

    for kandydat in KANDYDACI:
        print(f"\n=== {kandydat['dostawca']}/{kandydat['model']} ===")
        start = time.time()
        wynik = zapytaj_model(wiadomosci, kandydaci=[kandydat])
        czas = time.time() - start

        if wynik is None:
            print(f"--- NIEDOSTEPNY (po {czas:.0f} s)")
            continue

        print(wynik["tekst"])
        print(f"--- czas: {czas:.1f} s | zuzycie: {wynik['zuzycie']}")