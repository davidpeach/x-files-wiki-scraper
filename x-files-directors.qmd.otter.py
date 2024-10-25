
















from bs4 import BeautifulSoup
import requests
import csv


class Episode:
    def __init__(self, series):
        self.series = series

    def getseries(self):
        return self.series

    def settitle(self, title):
        self.title = title

    def gettitle(self):
        return self.title

    def setnumoverall(self, numoverall):
        self.numoverall = numoverall

    def getnumoverall(self):
        return self.numoverall

    def setnuminseries(self, numinseries):
        self.numinseries = numinseries

    def getnuminseries(self):
        return self.numinseries

    def setdirector(self, director):
        self.director = director

    def getdirector(self):
        return self.director

    def setwriter(self, writer):
        self.writer = writer

    def getwriter(self):
        return self.writer

    def setairdate(self, airdate):
        self.airdate = airdate

    def getairdate(self):
        return self.airdate

    def setprodcode(self, prodcode):
        self.prodcode = prodcode

    def getprodcode(self):
        return self.prodcode

    def setviewersus(self, viewersus):
        self.viewersus = viewersus

    def getviewersus(self):
        return self.viewersus


episodes_url = "https://en.wikipedia.org/wiki/List_of_The_X-Files_episodes"

page = requests.get(episodes_url)
soup = BeautifulSoup(page.text, features="html.parser")
series_tables = soup.find_all("table", class_="wikiepisodetable")

# Remove the tables for the two films.
del series_tables[5]
del series_tables[9]

all_episodes = []
series_counter = 0
for series in series_tables:
    series_counter += 1

    for episode in series.find_all("tr", class_="vevent"):
        ep = Episode(series_counter)
        ep.setnumoverall(episode.find("th").text)

        info_columns = episode.findAll("td")

        ep.setnuminseries(info_columns[0].text)
        # TODO: handle some odd table cells 🥴
        if ep.getnumoverall() == 201202:
            continue

        ep.settitle(info_columns[1].text.replace('"', ""))
        ep.setdirector(info_columns[2].text)
        ep.setwriter(info_columns[3].text)
        ep.setairdate(info_columns[4].text)
        ep.setprodcode(info_columns[5].text)
        ep.setviewersus(info_columns[6].text)

        all_episodes.append(ep)

filename = "x-files-episodes.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "title",
            "numoverall",
            "series",
            "numinseries",
            "director",
            "writer",
            "airdate",
            "viewers",
        ]
    )
    for ep in all_episodes:
        writer.writerow(
            [
                ep.gettitle(),
                ep.getnumoverall(),
                ep.getseries(),
                ep.getnuminseries(),
                ep.getdirector(),
                ep.getwriter(),
                ep.getairdate(),
                ep.getviewersus(),
            ]
        )

