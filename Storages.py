import json
import re
import datetime

from Entity import *
from common import *

class MatchesStorage:
    def __init__(self, sources):
        self.matches = []
        self.hash2matchInd = dict()
        self.oneVSone = dict()

        self.matchesDict = dict()
        self.sourceMatches = dict()
        self.playerMatches = dict()
        self.compNamesPairs = set()
        for source, filename in sources:
            self.sourceMatches[source] = []
            print(filename)
            with open(filename, encoding='utf-8') as fin:
                headerTokens = next(fin).strip().split('\t')
                headerDict = dict(zip(headerTokens, range(len(headerTokens))))
                for line in fin:
                    tokens = [e.rstrip() for e in line.split('\t')]
                    round = tokens[headerDict['round']] if 'round' in headerDict else None
                    matchId = tokens[headerDict['matchId']] if 'matchId' in headerDict else None
                    match = Match(tokens[headerDict['date']],
                                  [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')],
                                  names=[tokens[headerDict['name1']].split(';'), tokens[headerDict['name2']].split(';')],
                                  setsScore=tokens[headerDict['setsScore']],
                                  pointsScore=tokens[headerDict['pointsScore']],
                                  time=tokens[headerDict['time']],
                                  compName=tokens[headerDict['compName']],
                                  source=source,
                                  round=round,
                                  matchId=matchId)
                    self.addMatch(source, match)

    def addMatch(self, source, match):
        if match.date < '2014':
            return
        if source not in self.sourceMatches:
            self.sourceMatches[source] = []
        self.sourceMatches[source].append(match)

        for i in range(2):
            for e in match.ids[i]:
                if e not in {'-', '?'}:
                    if e not in self.playerMatches:
                        self.playerMatches[e] = dict()
                    if source not in self.playerMatches[e]:
                        self.playerMatches[e][source] = dict()
                    if match.date not in self.playerMatches[e][source]:
                        self.playerMatches[e][source][match.date] = []
                    self.playerMatches[e][source][match.date].append(match)

        # print('MatcheStorage.addMatch', match.hash, match.hash in self.matchesDict)
        if match.hash not in self.matchesDict:
            if match.hash not in self.matchesDict:
                self.matchesDict[match.hash] = []
            self.matchesDict[match.hash].append(match)
            self.matches.append(match)

            self.hash2matchInd[match.hash] = len(self.matches) - 1

            if match.isPair == 0:
                if match.getMW() in {'mm', 'ww'}:
                    pp = min(match.ids[0][0], match.ids[1][0]) + '\t' + max(match.ids[0][0], match.ids[1][0])
                    if pp not in self.oneVSone:
                        self.oneVSone[pp] = [match]
                    else:
                        self.oneVSone[pp].append(match)
#                    print(line)

            return True
        else:
            self.matchesDict[match.hash][0].addSource(match.sources[0])
            if self.matchesDict[match.hash][0].compName != match.compName:
                self.compNamesPairs.add(self.matchesDict[match.hash][0].compName + ' === ' + match.compName)

        return False

    def getMatches(self, source=None):
        if source is None:
            return self.matches
        return self.sourceMatches[source]

    def isActive(self, playerId, source, date):
        return date in self.playerMatches.\
            get(playerId, dict()).\
            get(source, dict())

    def buildHash2MatchInd(self):
        for i, match in enumerate(self.matches):
            self.hash2matchInd[match.hash] = i

    def getOneVSOneMatches(self, p1, p2, curDate, curTime, ws=1):
        if curTime is None:
            curTime = '00:00'
        result = []
        pp = min(p1, p2) + '\t' + max(p1, p2)
        leftDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=ws)).strftime("%Y-%m-%d")
        for match in sorted(self.oneVSone.get(pp, []), key=lambda x: x.date + ' ' + (x.time if not (x.time is None) else '99:99')):
            matchTime = (match.time if not (match.time is None) else '99:99')
            if match.date >= leftDate and match.date + ' ' + matchTime < curDate + ' ' + curTime:
                if p1 not in match.ids[0]:
                    match = match.reverse()
                result.append(match)
        return result


class CompetitionsStorage:
    def __init__(self):
        self.competitionsDict = dict()
        self.competitions = []

    def getCompId(self, compName):
        if not (compName in self.competitionsDict):
            self.competitions.append(Competition(len(self.competitionsDict), compName))
            self.competitionsDict[compName] = len(self.competitionsDict)
        return self.competitionsDict[compName]

    def getCompName(self, compId):
        try:
            if int(compId) < len(self.competitions):
                return self.competitions[int(compId)].name
        except:
            pass
        return None

    def getComp(self, compId):
        try:
            if int(compId) < len(self.competitions):
                return self.competitions[int(compId)]
        except:
            pass
        return None


from rankingCalc import *

class RankingsStorage:
    def __init__(self, sources):
        self.rankings = dict()
        self.dateRankings = dict()
        self.dayRankings = dict()
        self.dayRankingsLastDate = None
        self.dayRankingsModels = dict()

        for source, filename in sources:
            self.rankings[source], self.dateRankings[source] = RankingsStorage.readPlayersRankings(filename)

    def getRanking(self, playerId, source, curDate, ws=1):
        #[leftDate = curDate - ws < date <= curDate]
        leftDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=ws)).strftime("%Y-%m-%d")
        r = -1
        if playerId in self.rankings[source]:
            for e in sorted(self.rankings[source][playerId].items(), key=lambda x: x[0], reverse=True):
                if leftDate < e[0] <= curDate:
                    r = e[1][0]
                    break
            if r == '-100':
                r = -1
        r = float(r)
        return r

    def getRankings(self, playerId, curDate, ws=1):
        res = dict()
        for source in self.rankings:
            res[source] = self.getRanking(playerId, source, curDate, ws=ws)
        return res

    def getPlayersRankings(self, source, curDate, mw, ws=1):
        r = [float('nan')] * 20000
        for i in range(ws):
            leftDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - \
                        datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if leftDate in self.dateRankings[source]:
                for playerId, values in self.dateRankings[source][leftDate].items():
                    if playerId[0] == mw:
                        r[int(playerId[1:]) - 1] = float(values[0])
                break

        return r

    def getPlayerAllRankings(self, playerId, source):
        r = dict()
        if playerId in self.rankings[source]:
            r = self.rankings[source][playerId]
        return r

    def readPlayersDayRankings(self, source, filename):
        if source not in self.dayRankings:
            self.dayRankings[source] = dict()
        #dateRankings = dict()
        with open(filename, 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                playerId = tokens[2]
                if playerId not in self.dayRankings[source]:
                    self.dayRankings[source][playerId] = dict()
                dt = tokens[0] + ' ' + tokens[1]
                self.dayRankings[source][playerId][dt] = tokens[4]
                if self.dayRankingsLastDate is not None:
                    self.dayRankingsLastDate = max(self.dayRankingsLastDate, tokens[0])
                else:
                    self.dayRankingsLastDate = tokens[0]
                #if dt not in dateRankings:
                #    dateRankings[dt] = dict()
                #dateRankings[tokens[0]][tokens[1]] = tokens[2:]
        #return playersRankings, dateRankings

    def getDayRanking(self, playerId, source, curDate, curTime, ws=1):
        #[leftDAte = curDate - ws < date <= curDate]
        #leftDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=ws)).strftime("%Y-%m-%d")
        r = -100
        if playerId in self.dayRankings[source]:
            for e in sorted(self.dayRankings[source][playerId].items(), key=lambda x: x[0], reverse=True):
                eDate = e[0][:10]
                eTime = e[0][11:]
                if eDate == curDate:
                    if eTime < curTime:
                        r = e[1]
                        break
            if r == '-100':
                r = -100
        r = float(r)
        if r == -100:
            return self.getRanking(playerId, source.replace('_day', ''), curDate, ws=ws)
        return r

    def addMatch(self, source, match):
        if match.date > self.dayRankingsLastDate:
            mw = match.getMW()
            if mw not in {'mm', 'ww'}:
                return
            mw = mw[0]
            print('matchesStorage.addMatch', match.toStr())
            for rName in self.dayRankings:
                oldRankings = self.getPlayersRankings(rName.replace('_day', ''), match.date, mw, ws=100)
                if rName not in self.dayRankingsModels:
                    self.dayRankingsModels[rName] = dict()
                if match.date not in self.dayRankingsModels[rName]:
                    self.dayRankingsModels[rName][match.date] = dict()
                if mw not in self.dayRankingsModels[rName][match.date]:
                    self.dayRankingsModels[rName][match.date][mw] = \
                        BradleyTerryRM(oldRankings=oldRankings)

                # if match.hash == '9733076751776552711970068983':
                #     print(oldRankings)
                #     raise

                rm = self.dayRankingsModels[rName][match.date][mw]

                if match.isPair == 0 and (match.ids[0][0] + match.ids[1][0]).find(',') == -1:
                    print(match.toStr())
                    ind = [(int(e[1:]) - 1) for e in [match.ids[0][0], match.ids[1][0]]]
                    w = calcSetWeight(match)

                    if oldRankings[ind[0]] == oldRankings[ind[0]] and oldRankings[ind[1]] == oldRankings[ind[1]]:
                        rm.addMatches([[[ind[0]], [ind[1]]]], [1], [w])
#                            dayRankings[match.hash] = [[tr[mw][ind[0]]], [tr[mw][ind[1]]]]

                        rNew = rm.calcDayRankings()

                        print('DAY RANKINGS', rName)
                        for i in range(2):
                            playerId = match.ids[i][0]
                            if playerId not in self.dayRankings[rName]:
                                self.dayRankings[rName][playerId] = dict()
                            self.dayRankings[rName][playerId][match.date + ' ' + match.time] = rNew[ind[i]]
                            self.dayRankings[rName][playerId][match.date + ' ' + match.time] = rNew[ind[i]]
                            print(match.names[i][0], oldRankings[ind[i]], rNew[ind[i]])


    @staticmethod
    def readPlayersRankings(filename):
        filenames = [filename]
        if isinstance(filename, list):
            filenames = filename
        playersRankings = dict()
        dateRankings = dict()
        for filename in filenames:
            with open(filename, 'r', encoding='utf-8') as fin:
                for line in fin:
                    tokens = line.split('\t')
                    tokens = [e.strip() for e in tokens]
                    if len(tokens[0]) == 7:
                        tokens[0] += '-01'
                    if tokens[1] not in playersRankings:
                        playersRankings[tokens[1]] = dict()
                    playersRankings[tokens[1]][tokens[0]] = tokens[2:]
                    if tokens[0] not in dateRankings:
                        dateRankings[tokens[0]] = dict()
                    dateRankings[tokens[0]][tokens[1]] = tokens[2:]
        return playersRankings, dateRankings


