import hashlib
import json
import numpy as np
from common import *

class MatchBet:
    def __init__(self, eventId, dt, compName, ids, eventsInfo, players=None, segment="segment"):
        self.eventId = eventId
        self.dt = dt
        self.compName = compName
        self.ids = ids
        self.eventsInfo = eventsInfo
        self.players = players
        self.segment = segment

    def __str__(self):
        return '\t'.join([self.eventId, self.dt, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]),
                         json.dumps(self.eventsInfo, ensure_ascii=False)])

    def getKey(self):
        return calcHash([self.compName, str(self.eventId)])

    def toDict(self):
        res = dict()
        res['key'] = self.getKey()
        res['date'] = self.dt
        res['ids'] = [e.copy() for e in self.ids]
        res['players'] = [e.copy() for e in self.players]
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

    def merge(self, matchBet):
        if self.compName != matchBet.compName:
            print(self.compName, matchBet.compName)
#            raise
        if ';'.join(self.players[0]) != ';'.join(matchBet.players[0]):
            raise
        if ';'.join(self.players[1]) != ';'.join(matchBet.players[1]):
            raise
        if self.dt < matchBet.dt:
            #self.ts = self.ts + matchBet.ts
            self.eventsInfo = self.eventsInfo + matchBet.eventsInfo
        else:
            self.dt = matchBet.dt
            #self.ts = matchBet.ts + self.ts
            self.eventsInfo = matchBet.eventsInfo + self.eventsInfo
        return self


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
            for e in match.players[i]:
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

class Player:
    def __init__(self, id, names, mw):
        self.id = id
        self.names = names
        self.name = names[0]
        self.mw = mw
        self.matches = []

    def findString(self, s):
        for name in self.names:
            if name.lower().find(s.lower()) != -1:
                return True
        return False

class Match:
    '''
    def __init__(self, date, isPair, players, wins, sets, setsScore, time = '12:00', points = [-1, -1], pointsScore = ''):
        self.date = date
        self.time = time
        self.isPair = isPair
        self.players = players
        self.wins = wins
        self.sets = sets
        self.setsScore = setsScore
        self.points = points
        self.pointsScore = pointsScore
    '''

    def __init__(self, date, players, matchId = None, winsScore = None, setsScore = None, pointsScore=None,
                 time=None, isPair = None, compName = None, source = None, round = None):
        self.date = date
        self.players = players
        self.matchId = matchId
        self.flError = 0

        self.sources = []

        self.round = round

        self.winsScore = winsScore
        self.wins = None
        self.setsScore = setsScore
        self.sets = None
        self.pointsScore = pointsScore
        self.points = None

        if (self.setsScore is None) and not (self.pointsScore is None):
            self.sets, self.points = Match.getPointsScoreInfo(self.pointsScore)
            self.setsScore = str(self.sets[0]) + ':' + str(self.sets[1])
        if not (self.setsScore is None) and (self.sets is None):
            try:
                self.sets = [int(e) for e in self.setsScore.split(':')]
            except:
                self.flError = 1
                pass
        if not (self.pointsScore is None) and (self.points is None):
            try:
                _, self.points = Match.getPointsScoreInfo(self.pointsScore)
            except:
                self.flError = 1
                pass

        if (self.winsScore is None) and not (self.sets is None):
            self.wins = [int(self.sets[0] > self.sets[1]), int(self.sets[1] > self.sets[0])]
            self.winsScore = str(self.wins[0]) + ':' + str(self.wins[1])
        if not (self.winsScore is None) and (self.wins is None):
            self.wins = [int(e) for e in self.winsScore.split(':')]

        self.compName = compName
        self.compId = None
        self.sources.append(source)
        self.time = time
        self.isPair = isPair
        if (self.isPair is None):
            self.isPair = 0
            if len(self.players[0]) == 2:
                self.isPair = 1

        self.hash = self.getHash()

    def setCompId(self, compId):
        self.compId = compId

    def addSource(self, source):
        if not (source in self.sources):
            self.sources.append(source)

    def getHash(self):
        if self.sets is None:
            sets = []
        else:
            sets = self.sets
        return calcHash([self.date] + self.players[0] + self.players[1] + sets + [e * i for i,e in enumerate(Match.getSetSumPoints(self.points))])
        #return calcHash([self.date, self.round] + self.players[0] + self.players[1] + sets + [e * i for i,e in enumerate(Match.getSetSumPoints(self.points))])

    def reverse(self):
        matchReversed = Match(self.date, [self.players[1].copy(), self.players[0].copy()],
                              setsScore=Match.reverseSetsScore(self.setsScore),
                              pointsScore=Match.reversePointsScore(self.pointsScore))
        matchReversed.time = self.time
        matchReversed.compName = self.compName
        matchReversed.compId = self.compId
        matchReversed.sources = self.sources
        return matchReversed

    def toStr(self):
        return '\t'.join([self.date, self.time, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]), str(self.setsScore), str(self.pointsScore)])

    def toArr(self):
        return [self.date, self.time, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]), str(self.setsScore), str(self.pointsScore)]

    def toDict(self):
        res = dict()
        res['hash'] = self.hash
        res['date'] = self.date
        res['players'] = [e.copy() for e in self.players]
        res['setsScore'] = self.setsScore
        res['pointsScore'] = self.pointsScore
        return res

    @staticmethod
    def getPointsScoreInfo(pointsScore):
        sets = [0, 0]
        points = [[],[]]
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
    def checkSetsScore(score):
        res = score in {'3:0', '3:1', '3:2', '2:3', '1:3', '0:3',
                        '4:0', '4:1', '4:2', '4:3', '3:4', '2:4', '1:4', '0:4'}
        return res

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


