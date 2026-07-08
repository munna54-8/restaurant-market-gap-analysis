import requests
from bs4 import BeautifulSoup

url = "https://www.zomato.com/bangalore/indiranagar-restaurants"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=15)
print("Status code:", response.status_code)
print("Length of HTML:", len(response.text))

with open("data/raw/test_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")
print("Page title:", soup.title.string if soup.title else "No title found")