import time
import random
from os import walk
from lxml import html
from lxml import etree
import pyodbc

from Entity import Match
from ParserBKFon import ParserBKFon
from master_tour_prepare import read_players


import mysql.connector
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',
                              database='ttstat')
cursor = cnx.cursor()
cursor.execute("SELECT * FROM sites")
for row in cursor.fetchall():
    print(row)
cnx.close()


def main():
    dir = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live/clean'

    players = set()
    
#    matches = ParserBKFon.parseOneSegment(dir + '/' + 'segment28824.txt') # master-tour mix
#    matches = ParserBKFon.parseOneSegment(dir + '/' + 'segment25827.txt') # master-tour women + CHINA?!
#    matches = ParserBKFon.parseOneSegment(dir + '/' + 'segment26989.txt') # St.Petersburg master-tour men
#    matches = ParserBKFon.parseOneSegment(dir + '/' + 'segment30240.txt') #Israel master-tour
#    matches = ParserBKFon.parseOneSegment(dir + '/' + 'segment18054.txt') # China master-tour women
    parserBKFon = ParserBKFon(dir + '/' + 'segment34654.txt')
#    matches = ParserBKFon.parseOneSegment(dir + '/' + 'segment34654.txt') # China master-tour men
#    print(matches.keys())
    print(len(parserBKFon.matches))

    (men_players, men2_players) = read_players('prepared_data/master_tour/master_tour_players_men.txt')
    (women_players, women2_players) = read_players('prepared_data/master_tour/master_tour_players_women.txt')
    
    for match in parserBKFon.matches:
#    for key,value in matches.items():
#        match = Match(value)
        for i in range(2):
            for j in range(len(match.players[i])):
                if not(match.players[i][j]) in women2_players and not(match.players[i][j]) in men2_players:
                    print(match.players[i])
#        players.add(match.players[0])
#        players.add(match.players[1])

        print(match.eventId)
        print(match.compName)
        print(match.players)
        for i in range(len(match.score)):
            print((match.score[i], match.bet_win[0][i], match.bet_win[1][i]))

#        print(match.score)
#        print(match.win[0])
#        print(match.win[1])
    
    return

#    for f in walk(dir):
#        for ff in f[2]:
#            if ff[:7] == 'segment':
#                print(ff)
#                ParserBKFon.parseOneSegment(dir + '/' + ff)
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