import json
import re
import datetime

from Entity import *
from common import *

class MatchesStorage:
    def __init__(self, sources):
        self.matches = []
        self.hash2matchInd = dict()

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
#                    print(line)
                    elif matchHash in matchesDict:
                        matchesDict[matchHash][0].addSource(source)
                        if matchesDict[matchHash][0].compName != match.compName:
                            compNamesPairs.add(matchesDict[matchHash][0].compName + ' === ' + match.compName)


class MatchesBetsStorage:
    def __init__(self, hash2matchInd):
        self.bets = dict()

        with open('prepared_data/bkfon/live/all_bets_prepared.txt', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.rstrip('\n').split('\t')
                eventId = tokens[1]
                dt = tokens[2]
                compName = tokens[3]
                ids = [tokens[4].split(';'), tokens[5].split(';')]
                info = json.loads(tokens[8])
                pattern = r"\(([A-Za-z0-9- ]+)\)"
                pointsScore = re.search(pattern, info[-1][1])
                points = None
                if not (pointsScore is None):
                    pointsScore = pointsScore.group(0).replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':') + ';'
                    _, points = Match.getPointsScoreInfo(pointsScore)
                setsScore = info[-1][1].split(' ')[0]
                matchHash = None
                if setsScore != '':
                    matchHash = calcHash([dt[:10]] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')] + [e * i for i, e in enumerate(Match.getSetSumPoints(points))])
                if matchHash in hash2matchInd:
                    ts = []
                    score = []
                    bet_win = [[], []]
                    for i in range(len(info)):
                        ts.append(info[i][0])
                        score.append(info[i][1])
                        bet_win[0].append(info[i][2][0])
                        bet_win[1].append(info[i][2][1])
                    matchBet = MatchBet(eventId, [], dt, compName, ids, ts, score, bet_win)
                    if not (matchHash in self.bets):
                        self.bets[matchHash] = matchBet
                    else:
                        print('not unique bet match hash')

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
