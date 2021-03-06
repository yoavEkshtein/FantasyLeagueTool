import requests
from bs4 import BeautifulSoup
import html

class player:
    def __init__(self, name, peff, pprice, ppos, pratio, leagueteam):
        self.name = name
        self.leagueteam = leagueteam
        self.pos = ppos
        self.price = pprice
        self.ratio = pratio
        self.eff = peff
        self.teamratio = 0.0

    def getratiobyclub(self, clubs):
        for someclub in clubs:
            if someclub.name == self.leagueteam:
                if self.pos == 'מאמן':
                    self.teamratio = someclub.ratio * 10
                else:
                    self.teamratio = someclub.ratio * 5

class club():
    def __init__(self, name, wins, losses):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.ratio = ''

    def calculate_ratio(self):
        self.ratio = int(self.wins) / (int(self.losses) + int(self.wins))
        float(self.ratio)


def fill_player_list():
    players = []
    statsurl = 'http://basket.co.il/Game/search.asp?mode=2'
    r = requests.get(statsurl)
    sitedata = r.content.decode('cp1255')
    soup = BeautifulSoup(sitedata, 'html.parser')
    agg = soup.find_all('tr', attrs={'style': 'border-bottom:Solid 1px #ccc;'})
    for row in agg:
        segs = row.text.split()
        if segs.__len__() == 7:
            price = float(segs[0])
            eff = float(segs[1])
            pos = segs[2]
            name = segs[3] + ' ' + segs[4]
            team = segs[5] + ' ' + segs[6]
            ratio = (float(eff)/float(price))
            players.append(player(name, eff, price, pos, ratio, team))
    return players

def getCoaches():
    coaches = []
    coachesurl = 'http://basket.co.il/Game/search.asp?name=&crole=4'
    r = requests.get(coachesurl)
    sitedata = r.content.decode('cp1255')
    soup = BeautifulSoup(sitedata, 'html.parser')
    agg = soup.find_all('tr', attrs={'style': 'border-bottom:Solid 1px #ccc;'})
    segs = []
    for row in agg:
        segs = row.text.split('\n')
        segs[0] = (segs[3].split('\xa0'))
        name = segs[0][0].lstrip()
        name = name.rstrip()
        pos = segs[2].lstrip()
        pos = pos.rstrip()
        coaches.append(player(name, 0, int(segs[1]), pos, 0, segs[0][1]))
    return coaches


def get_league_table():
    league_table = []
    tableurl = 'http://basket.co.il/StatsPage_table.asp'
    r = requests.get(tableurl)
    sitedata = r.content.decode('cp1255')
    soup = BeautifulSoup(sitedata, 'html.parser')
    agg = soup.find_all('table', attrs={'style': 'width:700px;text-align:center;direction:rtl;border:0px;padding:0px;margin:0px;border-collapse:collapse;vertical-align:top;'})
    htmltable = BeautifulSoup(str(agg[0]), 'html.parser')
    tablerows = htmltable.find_all('tr')
    for row in tablerows:
        splitrow = row.text.split('\n')
        if splitrow.__len__() == 27:
            clubtoadd = club(splitrow[2], splitrow[5], splitrow[6])
            clubtoadd.calculate_ratio()
            league_table.append(clubtoadd)
    return league_table


class inputs():
    def __init__(self):
        self.iterations = ''
        self.effcutoff = ''
        self.mintotratio = ''

    def calc_inputs(self, clinputs):
        try:
            self.iterations = int(clinputs[1])
        except:
            self.iterations = 2000
        try:
            self.effcutoff = float(clinputs[2])
        except:
            self.effcutoff = 120.0
        try:
            self.mintotratio = float(clinputs[3])
        except:
            self.mintotratio = 1.2