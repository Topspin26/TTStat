import hashlib
import numpy as np
from common import *

class MatchBet:
    def __init__(self, eventId, rows, dt, compName, players, ts, score, bet_win):
        self.eventId = eventId
        self.rows = rows
        self.dt = dt
        self.compName = compName
        self.players = players
        self.ts = ts
        self.score = score
        self.bet_win = bet_win

    def merge(self, matchBet):
        if self.compName != matchBet.compName:
            print(self.compName, matchBet.compName)
#            raise
        if ';'.join(self.players[0]) != ';'.join(matchBet.players[0]):
            raise
        if ';'.join(self.players[1]) != ';'.join(matchBet.players[1]):
            raise
        if self.dt < matchBet.dt:
            self.ts = self.ts + matchBet.ts
            self.score = self.score + matchBet.score
            self.bet_win = self.bet_win + matchBet.bet_win
        else:
            self.dt = matchBet.dt
            self.ts = matchBet.ts + self.ts
            self.score = matchBet.score + self.score
            self.bet_win = matchBet.bet_win + self.bet_win


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

    def __init__(self, date, players, winsScore = None, setsScore = None, pointsScore=None,
                 time=None, isPair = None, compName = None, source = None, round = None):
        self.date = date
        self.players = players
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
        self.sources.append(source)
        self.time = time
        self.isPair = isPair
        if (self.isPair is None):
            self.isPair = 0
            if len(self.players[0]) == 2:
                self.isPair = 1

        self.hash = self.getHash()

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
        matchReversed = Match(self.date, [self.players[1].copy(), self.players[0].copy()])
        matchReversed.time = self.time
        matchReversed.compName = self.compName
        matchReversed.sources = self.sources
        matchReversed.setsScore = Match.reverseSetsScore(self.setsScore)
        matchReversed.pointsScore = Match.reversePointsScore(self.pointsScore)
        return matchReversed

    def toStr(self):
        return '\t'.join([self.date, self.time, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]), str(self.setsScore), str(self.pointsScore)])

    def toArr(self):
        return [self.date, self.time, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]), str(self.setsScore), str(self.pointsScore)]

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


