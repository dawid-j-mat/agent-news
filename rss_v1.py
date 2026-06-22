import requests

url = "https://deepmind.google/blog/rss.xml"
odpowiedz = requests.get(url, timeout=10)

print(odpowiedz.status_code)
print(odpowiedz.text[:1500])