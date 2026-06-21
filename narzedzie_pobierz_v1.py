import requests
from bs4 import BeautifulSoup


def pobierz_tekst_ze_strony(url: str) -> str:
    """Pobiera strone internetowa pod podanym adresem URL i zwraca jej czysty tekst.

    Uzywaj tego narzedzia, gdy musisz przeczytac zawartosc konkretnej strony
    internetowej, na przyklad artykulu prasowego. Argument 'url' to pelny adres
    strony (zaczynajacy sie od http:// lub https://). Narzedzie zwraca sam tekst
    artykulu, bez znacznikow HTML. W razie problemu z pobraniem zwraca komunikat
    o bledzie zaczynajacy sie od 'BLAD:'.
    """
    try:
        odpowiedz = requests.get(url, timeout=10)
        odpowiedz.raise_for_status()
    except requests.exceptions.RequestException as blad:
        return f"BLAD: nie udalo sie pobrac strony {url}. Powod: {blad}"

    zupa = BeautifulSoup(odpowiedz.text, "html.parser")

    for znacznik in zupa(["script", "style"]):
        znacznik.decompose()

    czysty_tekst = zupa.get_text(separator="\n", strip=True)
    return czysty_tekst


if __name__ == "__main__":
    wynik = pobierz_tekst_ze_strony("https://example.com")
    print(wynik)