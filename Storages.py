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

        matchesDict = dict()
        compNamesPairs = set()
        for source, filename in sources:
            print(filename)
            with open(filename, encoding='utf-8') as fin:
                headerTokens = next(fin).strip().split('\t')
                headerDict = dict(zip(headerTokens, range(len(headerTokens))))
                for line in fin:
                    tokens = line.split('\t')
                    match = Match(tokens[headerDict['date']],
                                  [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')],
                                  setsScore=tokens[headerDict['setsScore']],
                                  pointsScore=tokens[headerDict['pointsScore']],
                                  time=tokens[headerDict['time']],
                                  compName=tokens[headerDict['compName']],
                                  source=source)
                    matchHash = match.getHash()
                    if not (matchHash in matchesDict) and match.date >= '2014':
                        if not matchHash in matchesDict:
                            matchesDict[matchHash] = []
                        matchesDict[matchHash].append(match)
                        self.matches.append(match)
                        self.hash2matchInd[matchHash] = len(self.matches) - 1
                        if match.isPair == 0:
                            pp = min(match.players[0][0], match.players[1][0]) + '\t' + max(match.players[0][0], match.players[1][0])
                            if not (pp in self.oneVSone):
                                self.oneVSone[pp] = [match]
                            else:
                                self.oneVSone[pp].append(match)
#                    print(line)
                    elif matchHash in matchesDict:
                        matchesDict[matchHash][0].addSource(source)
                        if matchesDict[matchHash][0].compName != match.compName:
                            compNamesPairs.add(matchesDict[matchHash][0].compName + ' === ' + match.compName)

    def getOneVSOneMatches(self, p1, p2, curDate, curTime, ws = 1):
        if curTime == None:
            curTime = '00:00'
        result = []
        pp = min(p1, p2) + '\t' + max(p1, p2)
        leftDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=ws)).strftime("%Y-%m-%d")
        for match in sorted(self.oneVSone.get(pp, []), key = lambda x: x.date + ' ' + (x.time if not (x.time is None) else '99:99')):
            matchTime = (match.time if not (match.time is None) else '99:99')
            if match.date >= leftDate and match.date + ' ' + matchTime < curDate + ' ' + curTime:
                if not (p1 in match.players[0]):
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

class MatchesBetsStorage:
    def __init__(self, hash2matchInd, dirname = ''):
        self.bets = dict()

        with open(dirname + 'prepared_data/bkfon/live/all_bets_prepared.txt', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.rstrip('\n').split('\t')
                eventId = tokens[1]
                dt = tokens[2]
                compName = tokens[3]
                ids = [tokens[4].split(';'), tokens[5].split(';')]
                info = json.loads(tokens[8])
                pattern = r"\(([A-Za-z0-9- ]+)\)"

                lastMatchInd = len(info) - 1
                while not ('match' in info[lastMatchInd][1]):
                    lastMatchInd -= 1
                    if lastMatchInd == -1:
                        break
                if lastMatchInd == -1:
                    print('bad info')
                    raise

                pointsScore = re.search(pattern, info[lastMatchInd][1]['match']['score'].replace('*', ''))
                points = None
                if not (pointsScore is None):
                    pointsScore = pointsScore.group(0).replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':') + ';'
                    _, points = Match.getPointsScoreInfo(pointsScore)
                setsScore = info[lastMatchInd][1]['match']['score'].split(' ')[0]

                #print(info[-1][1], pointsScore)

                if tokens[-1] != '':
                    pointsScoreFinal = tokens[-1] + ';'
                    setsScoreFinal = tokens[-2]
                    if points and pointsScoreFinal != pointsScore or setsScore != '' and setsScore != setsScoreFinal:
                        print(dt, compName, ids, setsScore, pointsScore, setsScoreFinal, pointsScoreFinal)
                        #raise
#                    if pointsScore is None or setsScore == '':
                        pointsScore = pointsScoreFinal
                        setsScore = setsScoreFinal
                        info.append(['final', {'match': {'score': setsScoreFinal + ' ' + pointsScoreFinal}}])
                        _, points = Match.getPointsScoreInfo(pointsScoreFinal)

                matchHash = None
                if setsScore != '':
                    try:
                        matchHash = calcHash([dt[:10]] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')] + [e * i for i, e in enumerate(Match.getSetSumPoints(points))])
                    except:
                        print(dt, compName, ids, setsScore, pointsScore, setsScoreFinal, pointsScoreFinal, info)
                        raise
                if matchHash in hash2matchInd:
                    ts = []
                    score = []
                    bet_win = [[], []]

                    ts = []
                    eventsInfo = []
                    for i in range(len(info)):
                        ts.append(info[i][0])
                        eventsInfo.append(info[i][1])
                    matchBet = MatchBet(eventId, [], dt, compName, ids, ts, eventsInfo)
                    if not (matchHash in self.bets):
                        self.bets[matchHash] = matchBet
                    else:
                        print('not unique bet match hash')
                        print([dt] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')])

class RankingsStorage:
    def __init__(self, sources):
        self.rankings = dict()
        for source, filename in sources:
            self.rankings[source] = RankingsStorage.readPlayersRankings(filename)

    def getRankings(self, playerId, source, curDate, ws = 1):
        #[leftDAte = curDate - ws < date <= curDate]
        leftDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=ws)).strftime("%Y-%m-%d")
        r = -1
        if playerId in self.rankings[source]:
            for e in sorted(self.rankings[source][playerId].items(), key = lambda x: x[0], reverse=True):
                if e[0] > leftDate and e[0] <= curDate:
                    r = e[1][0]
                    break
            if r == '-100':
                r = -1
        r = float(r)
        return r

    def getPlayerAllRankings(self, playerId, source):
        r = dict()
        if playerId in self.rankings[source]:
            r = self.rankings[source][playerId]
        return r

    @staticmethod
    def readPlayersRankings(filename):
        playersRankings = dict()
        with open(filename, 'r', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                tokens = [e.strip() for e in tokens]
                if len(tokens[0]) == 7:
                    tokens[0] += '-01'
                if not(tokens[1] in playersRankings):
                    playersRankings[tokens[1]] = dict()
                playersRankings[tokens[1]][tokens[0]] = tokens[2:]
        return playersRankings
