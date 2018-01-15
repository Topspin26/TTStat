import hashlib
import json
import re
import numpy as np
import copy
from common import *


class SetStat:
    def __init__(self):
        self.isFinal = False
        self.events = dict()

    def add(self, t, d):
        self.events[t] = copy.deepcopy(d)


class MatchStat:
    def __init__(self, eventsInfo):
        self.sets = dict()
        self.events = dict()
        self.score = dict()
        self.setsCnt = 3

        for j in range(len(eventsInfo)):
            if 'match' in eventsInfo[j][1]:
                score = eventsInfo[j][1]['match']['score']
                self.score[j] = score
                if score.find('5сетов') != -1:
                    self.setsCnt = 3
                elif score.find('7сетов') != -1:
                    self.setsCnt = 4
                self.events[j] = copy.deepcopy(eventsInfo[j][1]['match'])

            sets, _, _ = MatchBet.parseScore(score)
            for e, d in eventsInfo[j][1].items():
                if e != 'match':
                    indSet = int(e[0])
                    if indSet not in self.sets:
                        self.sets[indSet] = SetStat()
                    self.sets[indSet].add(j, d)
                    if np.sum(sets) == 2 * (self.setCnt - 1):
                        #print(j, score, e, d, sets)
                        self.sets[indSet].isFinal = True

        for set in self.sets:
            if self.sets[set].isFinal:
                #print(set)
                for t, d in sorted(self.sets[set].events.items(), key=lambda x: x[0]):
                    sets, _, _ = MatchBet.parseScore(self.score[t])
                    if np.sum(sets) == set - 1:
                        for e in ['win1', 'win2']:
                            if e in d:
                                if tuple(self.events[t][e]) == (0, -1):
#                                    print(set, e, d[e])
                                    self.events[t][e] = d[e]
                                else:
                                    print(set, t, d, self.events[t][e])
                                    #raise


class MatchBet:
    def __init__(self, eventId, dt, compName, ids, eventsInfo, names=None, segment="segment", extraInfo=dict()):
        self.eventId = eventId
        self.dt = dt
        self.compName = compName
        self.ids = ids
        self.eventsInfo = eventsInfo
        self.names = names
        self.segment = segment
        self.match = None
        self.extraInfo = extraInfo

    def buildMatch(self):
        score = self.getLastScore()
        setsScore = pointsScore = None
        if score is not None:
            setsScore, pointsScore, setsCnt = MatchBet.parseScore(score, isParsed=False)
        self.match = Match(self.dt[:10], self.ids,
                           names=self.names,
                           setsScore=setsScore,
                           pointsScore=pointsScore,
                           time=self.dt[11:],
                           compName=self.compName,
                           source='bkfon_live')
        return self.match

    def getMatch(self):
        if self.match is None:
            self.buildMatch()
        return self.match

    def __str__(self):
        return '\t'.join([self.eventId, self.dt, self.compName, ';'.join(self.names[0]), ';'.join(self.names[1]),
                         json.dumps(self.eventsInfo, ensure_ascii=False)])

    def getKey(self):
        return 'l' + calcHash([self.compName, str(self.eventId)])

    def getDate(self):
        return self.dt[:10]

    def checkOnMerge(self, matchBet):
        if self.getDate() == matchBet.getDate() and \
           ' '.join([';'.join(self.names[i]) for i in range(2)]) == ' '.join([';'.join(matchBet.names[i]) for i in range(2)]):
            sets1, points1, _ = MatchBet.parseScore(self.getLastScore())
            sets2, points2, _ = MatchBet.parseScore(matchBet.getLastScore())
            if sets1[0] <= sets2[0] and sets1[1] <= sets2[1]:
                for i in range(2):
                    for j in range(min(len(points1[i]), len(points2[i])) - 1):
                        if points1[i][j] != points2[i][j]:
                            return False
                return True
        return False

    @staticmethod
    def parseScore(score, isParsed=True, defaultPointsScore=None):
        sets = [0, 0]
        points = [[0], [0]]

        setsCnt = None
        if score.find('5сетов') != -1:
            setsCnt = 3
        elif score.find('7сетов') != -1:
            setsCnt = 4

        pattern = r"\(([A-Za-z0-9- \*]+)\)"

        pointsScore = re.search(pattern, score)
        if pointsScore is not None:
            pointsScore = pointsScore.group(0). \
                              replace('(', ''). \
                              replace(')', ''). \
                              replace('*', ''). \
                              strip(). \
                              replace(' ', ';'). \
                              replace('-', ':') + ';'
            if isParsed is True:
                _, points = Match.getPointsScoreInfo(pointsScore)
                if len(points[0]) == 0:
                    points = [[0], [0]]
        else:
            print('BAD SCORE', score)
            pointsScore = defaultPointsScore
        setsScore = ' '.join(score.split()).split(' ')[0].replace('5сетов', '').replace('7сетов', '')

        if isParsed is True:
            try:
                sets = [int(e) for e in setsScore.split(' ')[0].split(':')]
            except:
                pass
            return sets, points, setsCnt

        return setsScore, pointsScore, setsCnt

    @staticmethod
    def isFinalScore(score):
        if score is None:
            return False

        setsScore, pointsScore, setsCnt = MatchBet.parseScore(score, isParsed=False)

        if Match.checkSetsScore(setsScore, setsCnt=setsCnt) is False:
            return False
        return True


    def toDict(self):
        res = dict()
        res['key'] = self.getKey()
        res['date'] = self.dt
        res['ids'] = [e.copy() for e in self.ids]
        res['names'] = [e.copy() for e in self.names]
#        res['setsScore'] = self.setsScore
#        res['pointsScore'] = self.pointsScore
        return res

#    def calcHash(self):
#        return calcHash([self.dt[:10]] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')] + \
#                                             [e * i for i, e in enumerate(Match.getSetSumPoints(points))])

    def getLastScore(self):
        lastMatchInd = len(self.eventsInfo) - 1
        while 'match' not in self.eventsInfo[lastMatchInd][1]:
            try:
                if 'match' in self.eventsInfo[lastMatchInd][1][0]:
                    return self.eventsInfo[lastMatchInd][1][0]['match'].get('score', None)
            except:
                pass
            lastMatchInd -= 1
            if lastMatchInd == -1:
                break
        if lastMatchInd == -1:
            return None
        return self.eventsInfo[lastMatchInd][1]['match'].get('score', None)

    def from_str(self, s):
        tokens = s.split('\t')
        self.segment = tokens[0]
        self.eventId = tokens[1]
        self.dt = tokens[2]
        self.compName = tokens[3]
        self.ids = [tokens[4].split(';'), tokens[5].split(';')]
        self.eventsInfo = json.loads(tokens[6])

    def merge(self, matchBet, isSplitEvent=False):
        if self.compName != matchBet.compName:
            print(self.compName, matchBet.compName)
#            raise
        if ';'.join(self.names[0]) != ';'.join(matchBet.names[0]):
            with open('entity_names.txt', 'a') as flog:
                flog.write(str(self.names) + '\n')
                flog.write(str(matchBet.names) + '\n')
            print(self.names[0], self.names[1])
            print(matchBet.names[0], matchBet.names[1])
#            if self.names[0][0] != 'Гинзбург Ш' and \
#               self.names[0][0] != 'Медвецкая А' and \
#               self.names[0][0] != 'Пан И Ц' and \
#               self.names[0][0] != 'Game 2 Египет А  (ж)':
#                raise
            self.names = matchBet.names
        if ';'.join(self.names[1]) != ';'.join(matchBet.names[1]):
            with open('entity_names.txt', 'a') as flog:
                flog.write(str(self.names) + '\n')
                flog.write(str(matchBet.names) + '\n')
            print(self.names[0], self.names[1])
            print(matchBet.names[0], matchBet.names[1])
#            if self.names[1][0] != 'Мольнар Ч' and \
#               self.names[1][0] != 'Желубенков А' and \
#               self.names[1][0] != 'Какунина Я':
#                raise
            self.names = matchBet.names
        if self.dt < matchBet.dt:
            splitEvent = [[matchBet.eventsInfo[0][0], {}]] if isSplitEvent is True else []
            self.eventsInfo = self.eventsInfo + \
                              splitEvent + \
                              matchBet.eventsInfo
        else:
            self.dt = matchBet.dt
            splitEvent = [[self.eventsInfo[0][0], {}]] if isSplitEvent is True else []
            self.eventsInfo = matchBet.eventsInfo + \
                              splitEvent + \
                              self.eventsInfo
        return self


class Match:
    def __init__(self, date, ids, names=None, matchId=None, winsScore=None, setsScore=None, pointsScore=None,
                 time=None, isPair=None, compName=None, source=None, round=None):
        self.date = date
        self.ids = ids
        self.names = names
        self.matchId = matchId
        self.flError = 0

        self.sources = list()
        self.hrefs = dict()

        self.round = round

        self.winsScore = winsScore
        self.wins = None
        self.setsScore = setsScore
        self.sets = None
        self.pointsScore = pointsScore.rstrip(';') if pointsScore else pointsScore
        self.points = None

        if (self.setsScore is None) and (self.pointsScore is not None):
            self.sets, self.points = Match.getPointsScoreInfo(self.pointsScore)
            self.setsScore = str(self.sets[0]) + ':' + str(self.sets[1])
        if (self.setsScore is not None) and (self.sets is None):
            try:
                self.sets = [int(e) for e in self.setsScore.split(':')]
            except:
                self.flError = 1
                pass
        if (self.pointsScore is not None) and (self.points is None):
            try:
                _, self.points = Match.getPointsScoreInfo(self.pointsScore)
            except:
                # self.points = [[], []]
                self.flError = 1
                pass

        if (self.winsScore is None) and (self.sets is not None):
            self.wins = [int(self.sets[0] > self.sets[1]), int(self.sets[1] > self.sets[0])]
            self.winsScore = str(self.wins[0]) + ':' + str(self.wins[1])
        if not (self.winsScore is None) and (self.wins is None):
            self.wins = [int(e) for e in self.winsScore.split(':')]

        self.compName = compName
        self.compId = None
        self.sources.append(source)
        self.time = time
        self.isPair = isPair
        if self.isPair is None:
            self.isPair = 0
            if len(self.ids[0]) == 2:
                self.isPair = 1

        self.hash = self.getHash()

    def setCompId(self, compId):
        self.compId = compId

    def addSource(self, source):
        if not (source in self.sources):
            self.sources.append(source)

    def getMW(self):
        return ''.join(sorted(self.ids[0][0][:1] + self.ids[1][0][:1]))

    def getHash(self):
        if self.sets is None:
            sets = []
        else:
            sets = self.sets
        return calcHash([self.date] +
                        [e1 if e1 not in {'', '?', '-'} else e2 for e1, e2 in zip(self.ids[0], self.names[0])] +
                        [e1 if e1 not in {'', '?', '-'} else e2 for e1, e2 in zip(self.ids[1], self.names[1])] +
                        sets + [e * (i + 1) for i, e in enumerate(Match.getSetSumPoints(self.points))])

    def reverse(self):
        matchReversed = Match(self.date, [self.ids[1].copy(), self.ids[0].copy()],
                              names=[self.names[1].copy(), self.names[0].copy()],
                              setsScore=Match.reverseSetsScore(self.setsScore),
                              pointsScore=Match.reversePointsScore(self.pointsScore))
        matchReversed.time = self.time
        matchReversed.compName = self.compName
        matchReversed.compId = self.compId
        matchReversed.sources = self.sources
        return matchReversed

    def toStr(self):
        return '\t'.join([self.date, self.time, self.compName, ';'.join(self.ids[0]), ';'.join(self.ids[1]),
                          str(self.setsScore), str(self.pointsScore), self.hash])

    def toArr(self, round=False):
        arr = [self.date, self.time, self.compName, ';'.join(self.ids[0]), ';'.join(self.ids[1]), str(self.setsScore), str(self.pointsScore)]
        if round is True:
            arr += [self.round]
        return arr

    def toDict(self):
        res = dict()
        res['hash'] = self.hash
        res['date'] = self.date
        res['time'] = self.time
        res['ids'] = [e.copy() for e in self.ids]
        res['names'] = [e.copy() for e in self.names]
        res['setsScore'] = self.setsScore
        res['pointsScore'] = self.pointsScore
        return res

    @staticmethod
    def getPointsScoreInfo(pointsScore):
        sets = [0, 0]
        points = [[], []]
        for e in pointsScore.replace(':;', '').strip().strip(';').split(';'):
            if e == ':':
                continue
            try:
                tt = e.split(':')
                p1 = int(tt[0])
                points[0].append(p1)
                p2 = int(tt[1])
                points[1].append(p2)
                sets[0] += int(p1 > p2)
                sets[1] += int(p2 > p1)
            except Exception as ex:
                #print(pointsScore)
                raise
        return [sets, points]

    @staticmethod
    def reversePointsScore(pointsScore):
        pointsScoreReversed = []
        for e in pointsScore.replace(':;', '').strip().strip(';').split(';'):
            if e == ':':
                pointsScoreReversed.append(':')
                continue
            try:
                tt = e.split(':')
                p1 = int(tt[0])
                p2 = int(tt[1])
                pointsScoreReversed.append(str(p2) + ':' + str(p1))
            except Exception as ex:
                pointsScoreReversed.append(e)
        return ';'.join(pointsScoreReversed)

    @staticmethod
    def checkSetScore(score):
        tt = score.split(':')
        res = True
        try:
            set1 = int(tt[0])
            set2 = int(tt[1])
            if min(set1, set2) < 0 or max(set1, set2) < 11:
                res = False
            if max(set1, set2) == 11:
                if min(set1, set2) > 9:
                    res = False
            else:
                if max(set1, set2) - min(set1, set2) != 2:
                    res = False
        except:
            res = False
        return res

    @staticmethod
    def reverseSetsScore(score):
        tt = score.split(':')
        try:
            set1 = int(tt[0])
            set2 = int(tt[1])
        except:
            return score
        return str(set2) + ':' + str(set1)

    @staticmethod
    def checkSetsScore(score, setsCnt=None):
        sets3 = {'3:0', '3:1', '3:2', '2:3', '1:3', '0:3'}
        sets4 = {'4:0', '4:1', '4:2', '4:3', '3:4', '2:4', '1:4', '0:4'}
        #print(score, setsCnt)
        return (setsCnt == 3 and score in sets3) or \
               (setsCnt == 4 and score in sets4) or \
               (setsCnt is None and score in (sets3 | sets4))

    @staticmethod
    def getSetSumPoints(points):
        if (points is None):
            return [0, 0]
        return np.array(points[0]) + np.array(points[1])

    def getSumPoints(self):
        if (self.points is None):
            return [0, 0]
        return [sum(self.points[0]), sum(self.points[1])]

    def getTotalPoints(self):
        return sum(self.points[0]) + sum(self.points[1])


class Player:
    def __init__(self, id, names, mw):
        self.id = id
        self.names = names
        self.name = names[0]
        self.mw = mw
        self.matches = list()
        self.hrefs = dict()

    def findString(self, s):
        for name in self.names:
            if name.lower().find(s.lower()) != -1:
                return True
        return False

    def addHref(self, source, href):
        self.hrefs[source] = href


class Competition:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.matches = []
        self.startDate = None
        self.finishDate = None
        self.playersSet = set()
        self.sources = []

    def addMatch(self, match):
        self.matches.append(match)

        for i in range(2):
            for e in match.ids[i]:
                self.playersSet.add(e)
        for e in match.sources:
            if not (e in self.sources):
                self.sources.append(e)

        if self.startDate is None:
            self.startDate = match.date
        else:
            self.startDate = min(self.startDate, match.date)
        if self.finishDate is None:
            self.finishDate = match.date
        else:
            self.finishDate = min(self.finishDate, match.date)
