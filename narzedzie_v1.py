from datetime import date

def podaj_dzisiejsza_date():
    """Zwraca dzisiejsza date w formacie RRRR-MM-DD."""
    dzisiaj = date.today()
    return dzisiaj.isoformat()

if __name__ == "__main__":
    print(podaj_dzisiejsza_date())