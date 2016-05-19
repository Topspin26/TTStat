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
        for i in range(min(1000, len(rows))):
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
            self.score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[@class='eventScore ']/text()")
            if len(self.event) > 0:
                print(self.event[0])
#                print(html.tostring(self.event[0], encoding='unicode'))
                
            self.win1 = tr.xpath("//td[@id = '" + trId + "win1']/text()")
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
#                    print(self.players)
            #print(html.tostring(tr, encoding='unicode', pretty_print=True))
#            print('-------------------------------')
#        print('#-------------------------------')
        
        

def main():
    dir = 'D:/Programming/SportPrognoseSystem/BetsParser/data'

    players = set()
    
    for f in walk(dir):
        for ff in f[2]:
            matches = dict()
            if ff[:7] == 'segment':
                print(ff)
                #ff = 'foo1.txt'
                trSegmentS = None
                lastEventId = None
                with open(dir + '/' + ff, 'r', encoding='utf-8') as filename:
                    k = 0
                    for line in filename:
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
                        if k == 2000:
                            break
#                    print(html.tostring(tree, encoding='unicode', pretty_print=True))
#                    for line in lines[190:]:
#                        tr = html.fromstring(line)
#                        print(html.tostring(tr, encoding='unicode', pretty_print=True))
#                        print(tr.xpath("//td[@class = 'eventCellName']"))
#                        print(tr.xpath("//td[@class = 'eventCellName']//div[@class = 'eventScore']"))
#                        print(tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div/text()"))
#                        print(tr.xpath("//td[@class = 'eventDataWrapperName']//div/text()"))
                    print(matches.keys())
                    print(len(matches))

                    for key,value in matches.items():
                        match = Match(value)
                        players.add(match.players[0])
                        players.add(match.players[1])
                        print(key)
                        print(match.compName)
                        print(match.players)
                    break
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