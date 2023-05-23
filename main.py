import requests
import json
import datetime
from bs4 import BeautifulSoup

costTotal = 0
counter = 0


def timeToUnix(time):  # 22.05.2023 um 12:38 Uhr
    arr = time.split(" um ")
    date = arr[0]
    ltime = arr[1].replace(" Uhr", "")
    # 19.05.2023 18:00
    formatted_datetime = datetime.datetime.strptime(f'{date} {ltime}', "%d.%m.%Y %H:%M")
    unix_datetime = datetime.datetime.timestamp(formatted_datetime)
    return int(unix_datetime)


def filterText(text):
    text = text.replace("(deutsch)", "") \
        .replace("EQS-News: ", "") \
        .replace("EQS-Adhoc: ", "") \
        .replace("EUR", "€").replace("\xa0%", "%") \
        .strip()
    return text


def scrapeTraderfox(URL):
    global costTotal
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    blogposts = soup.find_all("article", class_="card-body card-border")
    for post in blogposts:
        global counter
        counter = counter + 1
        time = post.find("time", class_="small text-primary fw-bold").text
        headline = post.find("h2", class_="h5")
        name = ""
        try:
            name = post.find("span", class_="badge bg-dark").find("a", class_="text-reset").text
        except:
            pass

        text = filterText(headline.find("a", class_="text-reset").text)

        if "EQS-Stimmrechte" not in text and "EQS-DD" not in text and name:
            json = {
                "date": timeToUnix(time),
                "company": name,
                "headline": text
            }
            r = requests.post("", json=json)

            headlineLength = len(text)
            costEach = round(headlineLength * 0.00000266666, 5)  # 0.00004
            costTotal = costTotal + costEach
            print(f'{counter}:{json}')


for i in range(1, 100):
    URL = "https://markets.traderfox.com/nachrichten/dpa-afx-compact/kategorie-2-11/seite-" + str(i)
    scrapeTraderfox(URL)

print("Kostet total: " + str(costTotal) + "€")
print(counter)
