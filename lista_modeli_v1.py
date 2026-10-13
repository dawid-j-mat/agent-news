import sys
import requests
from warstwa_modelu_v3 import DOSTAWCY

if len(sys.argv) < 2:
    print("Uzycie: python lista_modeli_v1.py NAZWA_DOSTAWCY [FILTR]")
    print("Dostepni dostawcy:", ", ".join(DOSTAWCY))
    raise SystemExit

nazwa = sys.argv[1]
filtr = sys.argv[2].lower() if len(sys.argv) > 2 else ""
dostawca = DOSTAWCY[nazwa]

naglowki = {}
if dostawca["klucz"]:
    naglowki["Authorization"] = f"Bearer {dostawca['klucz']}"

odpowiedz = requests.get(f"{dostawca['adres']}/models", headers=naglowki, timeout=30)
odpowiedz.raise_for_status()

identyfikatory = sorted(model["id"] for model in odpowiedz.json()["data"])
pasujace = [i for i in identyfikatory if filtr in i.lower()]

print(f"{nazwa}: {len(pasujace)} z {len(identyfikatory)} modeli pasuje do filtra '{filtr}'")
for identyfikator in pasujace:
    print("  ", identyfikator)