import requests
from bs4 import BeautifulSoup

url = "https://example.com"

try:
    odpowiedz = requests.get(url, timeout=10)
    odpowiedz.raise_for_status()

    zupa = BeautifulSoup(odpowiedz.text, "html.parser")

    for znacznik in zupa(["script", "style"]):
        znacznik.decompose()

    czysty_tekst = zupa.get_text(separator="\n", strip=True)

    print("--- DLUGOSC HTML (przed):", len(odpowiedz.text), "znakow ---")
    print("--- DLUGOSC TEKST (po):", len(czysty_tekst), "znakow ---")
    print()
    print(czysty_tekst)

except requests.exceptions.RequestException as blad:
    print("Nie udalo sie pobrac strony.")
    print("Powod:", blad)