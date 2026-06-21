import requests

url = "https://ta-strona-na-pewno-nie-istnieje-12345.com"

try:
    odpowiedz = requests.get(url, timeout=10)
    odpowiedz.raise_for_status()
    print("Sukces! Kod statusu:", odpowiedz.status_code)
    print(odpowiedz.text)
except requests.exceptions.RequestException as blad:
    print("Nie udalo sie pobrac strony.")
    print("Powod:", blad)