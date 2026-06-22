import feedparser


def pobierz_naglowki_z_rss(url: str) -> str:
    """Pobiera liste najnowszych naglowkow z kanalu RSS pod podanym adresem.

    Uzywaj tego narzedzia, gdy chcesz zobaczyc, jakie nowe artykuly lub wpisy
    ukazaly sie w danym zrodle, BEZ pobierania ich pelnej tresci. Argument 'url'
    to adres kanalu RSS (czesto konczy sie na /rss, /feed lub .xml). Narzedzie
    zwraca ponumerowana liste wpisow: dla kazdego tytul, link i krotka zajawke.
    Na podstawie tej listy mozna zdecydowac, ktore artykuly warto pobrac w
    calosci osobnym narzedziem. W razie problemu zwraca komunikat zaczynajacy
    sie od 'BLAD:'. Gdy kanal nie ma zadnych wpisow, informuje o tym wprost.
    """
    kanal = feedparser.parse(url)

    if not kanal.entries:
        if kanal.bozo:
            return f"BLAD: nie udalo sie odczytac kanalu RSS pod adresem {url}. Powod: {kanal.bozo_exception}"
        return f"Kanal RSS pod adresem {url} nie zawiera zadnych wpisow (moze byc pusty, np. w weekend)."

    linie = []
    for numer, wpis in enumerate(kanal.entries, start=1):
        tytul = wpis.get("title", "(brak tytulu)")
        link = wpis.get("link", "(brak linku)")
        zajawka = wpis.get("summary", "(brak zajawki)")
        linie.append(f"{numer}. {tytul}\n   Link: {link}\n   Zajawka: {zajawka}")

    return "\n\n".join(linie)


if __name__ == "__main__":
    wynik = pobierz_naglowki_z_rss("https://deepmind.google/blog/rss.xml")
    print(wynik)