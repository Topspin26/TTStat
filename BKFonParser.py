import time
from lxml import html

from Entity import MatchBet
import os
from os import walk
import re

class ParserBKFonNew:
    def __init__(self, dirname, filename, maxCnt=-1):
        self.matches = []
        self.matchesDict = dict()
        self.lastEventId = None
        self.lastUpdate = dict()
#        self.counter = 0
        self.maxCnt = maxCnt

    def addLineBlock(self, dt, lines):
        matchesDict = dict()
        trSegmentS = None
        lastEventId = None
        for line in lines:
            #print(line)
            #tokens = line.split('\t')
            #time = ''
            #if len(tokens) == 2:
            #    time = tokens[0]
            #    line = tokens[1]
            line = re.sub(r'\<\!--[^>]*--\>', '', line)
            tr = html.fromstring(line)
            cl = tr.get('class')
            if cl.find('table__row _type_segment _sport_3088') != -1:
                trSegmentS = line
                lastEventId = None
            else:
                if tr.getchildren()[0].get('class').find('_indent_2') == -1:
                    lastEventId = line.split('"table__event-number">')[1].split('<')[0].strip()
                    #print(lastEventId)
                    #lastEventId = tr.get('id')
                if not (lastEventId is None):
                    if not (lastEventId in matchesDict):
                        matchesDict[lastEventId] = [trSegmentS]
    #                    self.lastUpdate[lastEventId] = self.counter
                    matchesDict[lastEventId].append(line)
#                self.lastUpdate[lastEventId] = self.counter
        resultBlock = []
        for key, value in matchesDict.items():
            resultBlock.append(self.prepareMatch(key, dt, value))
        return resultBlock

        '''
        if self.counter % 10000 == 0:
            print([self.counter, len(self.matchesDict)])
            matchesNew = dict()
            for key, value in self.matchesDict.items():
                if (self.counter - self.lastUpdate[key]) > 5000:
                    print('key', key)
                    self.matches.append(self.prepareMatch(key, value))
                else:
                    matchesNew[key] = value
            self.matchesDict.clear()
            matches = matchesNew
            print([len(self.matches), len(matches)])

            #if self.counter == self.maxCnt:
            #    break
            # if k == 2000:
            #     break
        for key, value in self.matchesDict.items():
            print('key', key)
            self.matches.append(self.prepareMatch(key, value))
        '''

    def prepareMatch(self, eventId, dt, rows):
        players = None
        compName = None
        eventsInfo = []
        ts = []
        lastTime = None
        events = dict()
        for i in range(len(rows)):
            line = rows[i]
#            print(line)
            line = line.replace(' _type-active', '')
            tr = html.fromstring(line)
            if tr.get('class').find('table__row _type_segment _sport_3088') != -1:
                if compName is None:
                    compName = line.split('"table__title-text">')[1].split('<')[0]
                continue
            trId = line.split('"table__event-number">')[1].split('<')[0].strip()

            '''
            if lastTime != rows[i][0]:
                if not (lastTime is None):
                    ts.append(lastTime)
                    eventsInfo.append(events.copy())
                    #print(events)
                    events = dict()
            
            lastTime = rows[i][0]
            '''

            if tr.getchildren()[0].get('class').find('_indent_2') == -1:
                #the whole match
                name = 'match'
                if players is None:
                    #print(line)
                    arr = line.split('"table__match-title-text">')
                    if len(arr) > 1:
                        players = line.split('"table__match-title-text">')[1].split('<')[0]
                    else:
                        players = line.split('"table__event-number">')[1].split('</span>')[1].split('<')[0].strip()
                    players = players.split(' — ')  # defis
                    for j in range(2):
                        players[j] = players[j].split('/')
                    #print(players)
            else:
                arr = line.split('"table__match-title-text">')
                if len(arr) > 1:
                    name = line.split('"table__match-title-text">')[1].split('<')[0].strip()
                else:
                    name = line.split('"table__event-number">')[1].split('</span>')[1].split('<')[0].strip()
                name = name.replace('-й', '').replace('сет', 'set')
                    #certain set
            #print(name)
            events[name] = dict()

#                ts.append(rows[i][0])
            tscore = ''

            arr0 = line.split('"table__score">')
            if len(arr0) > 1:
                tscore = arr0[1].split('<')[0]
                if len(tscore) == 0:
                    arr0 = line.split('"table__score-normal">')
                    if len(arr0) > 1:
                        tscore = arr0[1].split('<')[0]
            arr1 = line.split('"table__label _style_blue" title="')
            if len(arr1) > 1:
                tscore += ' ' + ''.join(arr1[1].split('">')[0].split())
                tscore = tscore.strip()
            arr = line.split('"table__score-more">')
            if len(arr) > 1:
                tscore += ' ' + arr[1].split('<')[0]
            tscore = tscore.strip()
#            if tscore == '5сетов':
#                #print(line)
#                print(tscore)
#                if len(score) == 0:
#                    score = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventDataWrapper']//div[@class='eventScore eventScoreActive']/text()")
            if len(tscore) > 0:
                events[name]['score'] = tscore
            else:
                events[name]['score'] = ''

            tds = tr.xpath('//td')
            columns = ['', '', 'win1', 'win2', 'fora1', 'win_f1', 'fora2', 'win_f2', 'total', 'total_l', 'total_g']
            for i in [2, 3]:
                fl = (tds[i].get('class').find('blocked') == -1)
                if not (tds[i].text is None):
                    events[name][columns[i]] = [float(tds[i].text), 1 if fl else -1]
                else:
                    events[name][columns[i]] = [0, -1]
            for i in [5, 7]:
                fl = (tds[i].get('class').find('blocked') == -1)
                if not (tds[i].text is None):
                    events[name][columns[i]] = [float(tds[i - 1].text.replace('+','')), float(tds[i].text), 1 if fl else -1]
                else:
                    events[name][columns[i]] = [0, 0, -1]
            for i in [9, 10]:
                fl = (tds[i].get('class').find('blocked') == -1)
                if not (tds[i].text is None):
                    events[name][columns[i]] = [float(tds[8].text), float(tds[i].text), 1 if fl else -1]
                else:
                    events[name][columns[i]] = [0, 0, -1]

#        if not (lastTime is None):
#            ts.append(lastTime)
#        eventsInfo.append(events.copy())
        eventsInfo = events.copy()
        #print(events)
        return MatchBet(eventId, dt, compName, None, [dt, eventsInfo], players=players)

# self.createMatchesDict()
#    def createMatchesDict(self):
#        for match in self.matches:


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
        dt = rows[0][0]
        players = None
        compName = None
        eventsInfo = []
        ts = []
        lastTime = None
        events = dict()
#        score = []
#        bet_win = [[], []]
#        dt = rows[0][0]
#        ts = []
        for i in range(len(rows)):
            line = rows[i][1]
#            print(line)
            tr = html.fromstring(rows[i][1])
            cl = ' ' + tr.get('class') + ' '
            if cl.find(' trSegment ') != -1:
                if compName is None:
                    compName = tr.xpath("*//div[contains(@class, 'lineSegmentFlag')]/text()")
                    compName = ''.join(compName)
                continue

            trId = tr.get('id')

            if lastTime != rows[i][0]:
                if not (lastTime is None):
                    ts.append(lastTime)
                    eventsInfo.append(events.copy())
                    #print(events)
                    events = dict()

            lastTime = rows[i][0]

            if tr.get('class').find('level2') == -1:
                #the whole match
                name = 'match'
                if players is None:
                    players = tr.xpath("//td[@class = 'eventCellName']//div[@class='event']/text()")
                    if len(players) == 0:
                        players = tr.xpath("//td[@class = 'eventCellName']//div[@class='eventBlocked']/text()")
                    players = ''.join(players)
                    players = players.split(' — ')  # defis
                    for j in range(2):
                        players[j] = players[j].split('/')
                    print(players)
            else:
                name = tr.xpath("//div[@class='event']/text()")
                if len(name) == 0:
                    name = tr.xpath("//div[@class='eventBlocked']/text()")
                name = name[0].strip().replace('-й', '').replace('сет', 'set')

            events[name] = dict()

            if cl.find(' trEvent ') != -1 or cl.find(' trEventChild ') != -1:
                tscore = tr.xpath("//div[contains(@class, 'eventScore')]/text()")
                if len(tscore) > 0:
                    events[name]['score'] = tscore[0]
                else:
                    events[name]['score'] = ''

                tds = tr.xpath('//td')
                columns = ['', '', '', 'win1', 'draw', 'win2', 'win1draw', 'win1win2', 'win2draw', 'fora1', 'win_f1', 'fora2', 'win_f2', 'total', 'total_l', 'total_g']
#                for i in range(len(tds)):
#                    print(columns[i], tds[i].text, tds[i].get('class'))

                for i in [3, 5]:
                    fl = (tds[i].get('class').find('eventCellBlock') == -1)
                    if not (tds[i].text is None):
                        events[name][columns[i]] = [float(tds[i].text), 1 if fl else -1]
                    else:
                        events[name][columns[i]] = [0, -1]
                for i in [10, 12]:
                    fl = (tds[i].get('class').find('eventCellBlock') == -1)
                    if not (tds[i].text is None):
                        events[name][columns[i]] = [float(tds[i - 1].text.replace('+', '')), float(tds[i].text), 1 if fl else -1]
                    else:
                        events[name][columns[i]] = [0, 0, -1]
                for i in [14, 15]:
                    fl = (tds[i].get('class').find('eventCellBlock') == -1)
                    if not (tds[i].text is None):
                        events[name][columns[i]] = [float(tds[13].text), float(tds[i].text), 1 if fl else -1]
                    else:
                        events[name][columns[i]] = [0, 0, -1]

        if not (lastTime is None):
            ts.append(lastTime)
            eventsInfo.append(events.copy())
            #print(events)
        return MatchBet(eventId, [], dt, compName, players, ts, eventsInfo)

