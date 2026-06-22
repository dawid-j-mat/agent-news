import feedparser

url = "https://deepmind.google/blog/rss.xml"
kanal = feedparser.parse(url)

print("Tytul kanalu:", kanal.feed.title)
print("Liczba wpisow:", len(kanal.entries))
print("---")

for wpis in kanal.entries[:5]:
    print("TYTUL:", wpis.title)
    print("LINK:", wpis.link)
    print("OPIS:", wpis.summary)
    print("DATA:", wpis.published)
    print("---")