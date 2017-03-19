import time
from lxml import html

from Entity import MatchBet
import os
from os import walk

class ParserBKFon:
    def __init__(self, dirname, filename, maxCnt = -1):

        filenames = []
        for f in walk(dirname):
            for ff in f[2]:
                fp = os.path.abspath(os.path.join(f[0], ff))
                if fp.find(filename) != -1:
                    filenames.append(fp)

        self.matches = []
        matches = dict()
        trSegmentS = None
        lastEventId = None
        lastUpdate = dict()
        k = 0
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as fin:
                for line in fin:
                    tokens = line.split('\t')
                    time = ''
                    if len(tokens) == 2:
                        time = tokens[0]
                        line = tokens[1]
                    tr = html.fromstring(line)
                    cl = tr.get('class')
                    if cl == 'trSegment':
                        trSegmentS = [time, line]
                    else:
                        if cl.find('trEventChild') == -1:
                            lastEventId = tr.get('id')
                        if not (lastEventId in matches):
                            matches[lastEventId] = [trSegmentS]
                            lastUpdate[lastEventId] = k
                        matches[lastEventId].append([time, line])
                        lastUpdate[lastEventId] = k
                    k += 1

                    if k % 10000 == 0:
                        print([k, len(matches)])
                        matchesNew = dict()
                        for key, value in matches.items():
                            if (k - lastUpdate[key]) > 5000:
                                self.matches.append(self.prepareMatch(key, value))
                            else:
                                matchesNew[key] = value
                        matches.clear()
                        matches = matchesNew
                        print([len(self.matches), len(matches)])

                    if k == maxCnt:
                        break
        #            if k == 2000:
        #                break
        for key,value in matches.items():
            self.matches.append(self.prepareMatch(key, value))
        
#        self.createMatchesDict()
    
#    def createMatchesDict(self):
#        for match in self.matches:
            
        
    def prepareMatch(self, eventId, rows):
        players = None
        compName = None
        score = []
        bet_win = [[], []]
        dt = rows[0][0]
        ts = []
        for i in range(len(rows)):
            tr = html.fromstring(rows[i][1])
            cl = ' ' + tr.get('class') + ' '
            if compName is None:
                if cl.find(' trSegment ') != -1: 
                    compName = tr.xpath("*//div[contains(@class, 'lineSegmentFlag')]/text()")
                    compName = ''.join(compName)
#                    print(self.compName)
                    
#            self.score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[@class='eventScore']/text()")
            trId = tr.get('id')
            
            event = tr.xpath("//td[@class = 'eventCellName eventCellNameSub']//div[@class='event']/text()")
#            if len(self.event) > 0:
#                print(self.event[0])

#                print(html.tostring(self.event[0], encoding='unicode'))

            if cl.find(' trEvent ') != -1:
                ts.append(rows[i][0])
                tscore = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[contains(@class, 'eventScore')]/text()")
#                if len(score) == 0:
#                    score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[@class='eventScore eventScoreActive']/text()")
                if len(tscore) > 0:
                    score.append(str(tscore[0]))
                else:
                    score.append('')

                for j,winj in enumerate(['win1', 'win2']):
                    bet_winj = tr.xpath("//td[@id = '" + trId + winj + "']")
                    if len(bet_winj) > 0:
                        bet_winj_class = bet_winj[0].get('class') 
                        bet_winj = bet_winj[0].text
                        if bet_winj:
                            bet_winj = bet_winj.replace(u'\xa0', '')
                            fl = 0
                            if len(bet_winj_class) > 0:
                                if bet_winj_class.find(bet_winj) == -1:
                                    fl = 1
                        else:
                            fl = -1
                            bet_winj = 0
                        bet_win[j].append([float(bet_winj), fl])
                    else:
                        bet_win[j].append([0, -1])
                
            bets = tr.xpath("//td[@class = 'eventCellValue']/text()")
#            if len(self.score) > 0:
#                print(self.score)
#            if len(self.win1) > 0:
#                print(self.win1)
#            if len(self.bets) > 0:
#                print(self.bets)
            if players is None:
                if cl.find(' trEvent ') != -1:
                    players = tr.xpath("//td[@class = 'eventCellName']//div[@class='event']/text()")
                    if len(players) == 0:
                        players = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventBlocked']/text()")
                    players = ''.join(players)
                    players = players.split(' — ') #defis
                    for j in range(2):
                        players[j] = players[j].split('/')
            
        return MatchBet(eventId, [], dt, compName, players, ts, score, bet_win)
#        return MatchBet(eventId, rows, dt, compName, players, score, bet_win) 
#                    print(self.players)
            #print(html.tostring(tr, encoding='unicode', pretty_print=True))
#            print('-------------------------------')
#        print('#-------------------------------')
        
