import requests

url = "https://ta-strona-na-pewno-nie-istnieje-12345.com"

odpowiedz = requests.get(url)

print(odpowiedz.status_code)
print(odpowiedz.text)