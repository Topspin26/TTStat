import time
import random
from os import walk
from lxml import html
from lxml import etree
import pyodbc

import mysql.connector

cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',
                              database='ttstat')
cursor = cnx.cursor()
cursor.execute("SELECT * FROM sites")
for row in cursor.fetchall():
    print(row)
cnx.close()


class Match:
    def __init__(self, rows):
        self.rows = rows
        self.players = None
        self.compName = None
        self.score = []
        self.bet_win = [[], []]
        for i in range(len(rows)):
            tr = html.fromstring(rows[i][1])
            cl = ' ' + tr.get('class') + ' '
            if self.compName is None:
                if cl.find(' trSegment ') != -1: 
                    self.compName = tr.xpath("*//div[contains(@class, 'lineSegmentFlag')]/text()")
                    self.compName = ''.join(self.compName)
#                    print(self.compName)
                    
#            self.score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[@class='eventScore']/text()")
            trId = tr.get('id')
            

            self.event = tr.xpath("//td[@class = 'eventCellName eventCellNameSub']//div[@class='event']/text()")
#            if len(self.event) > 0:
#                print(self.event[0])

#                print(html.tostring(self.event[0], encoding='unicode'))

            if cl.find(' trEvent ') != -1:
                score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[contains(@class, 'eventScore')]/text()")
#                if len(score) == 0:
#                    score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[@class='eventScore eventScoreActive']/text()")
                self.score.append(score)
                
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
                        self.bet_win[j].append([float(bet_winj), fl])
                    else:
                        self.bet_win[j].append([0, -1])
                
            self.bets = tr.xpath("//td[@class = 'eventCellValue']/text()")
#            if len(self.score) > 0:
#                print(self.score)
#            if len(self.win1) > 0:
#                print(self.win1)
#            if len(self.bets) > 0:
#                print(self.bets)
            if self.players is None:
                if cl.find(' trEvent ') != -1:
                    self.players = tr.xpath("//td[@class = 'eventCellName']//div[@class='event']/text()")
                    if len(self.players) == 0:
                        self.players = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventBlocked']/text()")
                    self.players = ''.join(self.players)
                    self.players = self.players.split(' — ') #defis
                    for j in range(2):
                        self.players[j] = self.players[j].split('/')
#                    print(self.players)
            #print(html.tostring(tr, encoding='unicode', pretty_print=True))
#            print('-------------------------------')
#        print('#-------------------------------')
        

def parseOneSegment(filename):
    #ff = 'foo1.txt'
    matches = dict()
    trSegmentS = None
    lastEventId = None
    with open(filename, 'r', encoding='utf-8') as fin:
        k = 0
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
                matches[lastEventId].append([time, line])
            k += 1
            
            if k % 1000 == 0:
                print(k)
#            if k == 2000:
#                break
            
    return matches    

from master_tour_prepare import read_players

def main():
    dir = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live/clean'

    players = set()
    
#    matches = parseOneSegment(dir + '/' + 'segment28824.txt') # master-tour mix
#    matches = parseOneSegment(dir + '/' + 'segment25827.txt') # master-tour women + CHINA?!
#    matches = parseOneSegment(dir + '/' + 'segment26989.txt') # St.Petersburg master-tour men
#    matches = parseOneSegment(dir + '/' + 'segment30240.txt') #Israel master-tour
#    matches = parseOneSegment(dir + '/' + 'segment18054.txt') # China master-tour women
    matches = parseOneSegment(dir + '/' + 'segment34654.txt') # China master-tour men
    print(matches.keys())
    print(len(matches))

    (men_players, men2_players) = read_players('prepared_data/master_tour/master_tour_players_men.txt')
    (women_players, women2_players) = read_players('prepared_data/master_tour/master_tour_players_women.txt')
    
    for key,value in matches.items():
        match = Match(value)
        for i in range(2):
            for j in range(len(match.players[i])):
                if not(match.players[i][j]) in women2_players and not(match.players[i][j]) in men2_players:
                    print(match.players[i])
#        players.add(match.players[0])
#        players.add(match.players[1])

        print(key)
        print(match.compName)
        print(match.players)
        for i in range(len(match.score)):
            print((match.score[i], match.bet_win[0][i], match.bet_win[1][i]))

#        print(match.score)
#        print(match.win[0])
#        print(match.win[1])
    
    return

    for f in walk(dir):
        for ff in f[2]:
            if ff[:7] == 'segment':
                print(ff)
                parseOneSegment(dir + '/' + ff)
#    match = Match(matches['event5192677'])
#    with open('foo_out.txt', 'w') as fout:
#        for e in sorted(players):
#            fout.write(e + '\n')
    
    '''    
    fout = ''
    for e in eventsData:
        if e[0] != lastEventId:
            lastEventId = e[0]
            if fout != '':
                fout.close()
            fout = open(e[0] + '.txt', 'a', encoding='utf-8')
        fout.write(e[1] + '\n')
    if fout != '':
        fout.close()
    
    time.sleep(timeout)
    '''        
    return

if __name__ == "__main__":
    main()