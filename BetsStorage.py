import json
import re
import datetime

from Entity import *

class BetsStorage:
    def __init__(self):
        self.bets = dict()
        self.liveBets = dict()
        self.lastUpdate = dict()
        self.counter = 0

    def loadFromFile(self, filename):
        with open(filename, encoding='utf-8') as fin:
            for line in fin:
                tokens = line.rstrip('\n').split('\t')
                eventId = tokens[1]
                dt = tokens[2]
                compName = tokens[3]
                ids = [tokens[4].split(';'), tokens[5].split(';')]
                players = [tokens[6].split(';'), tokens[7].split(';')]
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
                    pointsScore = pointsScore.group(0).replace('(', '').replace(')', '').\
                                                                        replace(' ', ';').replace('-',':') + ';'
                    _, points = Match.getPointsScoreInfo(pointsScore)
                setsScore = info[lastMatchInd][1]['match']['score'].split(' ')[0]

                # print(info[-1][1], pointsScore)

                if tokens[-1] != '':
                    pointsScoreFinal = tokens[-1] + ';'
                    setsScoreFinal = tokens[-2]
                    if points and pointsScoreFinal != pointsScore or setsScore != '' and setsScore != setsScoreFinal:
                        print(dt, compName, ids, setsScore, pointsScore, setsScoreFinal, pointsScoreFinal)
                        # raise
                        #                    if pointsScore is None or setsScore == '':
                        pointsScore = pointsScoreFinal
                        setsScore = setsScoreFinal
                        info.append(['final', {'match': {'score': setsScoreFinal + ' ' + pointsScoreFinal}}])
                        _, points = Match.getPointsScoreInfo(pointsScoreFinal)

                matchHash = None
                if setsScore != '':
                    try:
                        matchHash = calcHash([dt[:10]] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')] + \
                                             [e * i for i, e in enumerate(Match.getSetSumPoints(points))])
                    except:
                        print(dt, compName, ids, setsScore, pointsScore, setsScoreFinal, pointsScoreFinal, info)
                        raise
                if matchHash is not None:
                    if matchHash not in self.bets:
                        matchBet = MatchBet(eventId, dt, compName, ids, info, players=players)
                        self.bets[matchHash] = matchBet
                    else:
                        print('not unique bet match hash')
                        print([dt] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')])
                        #raise

    '''
    def mergeWithMatches(self, hash2matchInd):
        for matchHash, 
            if matchHash in hash2matchInd:
                matchBet = MatchBet(eventId, dt, compName, ids, info)
                if not (matchHash in self.bets):
                    self.bets[matchHash] = matchBet
                else:
                    print('not unique bet match hash')
                    print([dt] + ids[0] + ids[1] + [int(e) for e in setsScore.split(':')])
    '''

    def isFinalScore(self, score):
        if score is None:
            return False
        if score.find('5сетов') != -1 or score.find('7сетов') != -1:
            return False
        score = score.replace('5сетов', '').replace('7сетов', '')
        arr = ' '.join(score.split()).split(' ')
        setsScore = arr[0]
        if Match.checkSetsScore(setsScore) is False:
            return False
        return True
#        pointsScore = arr[1].replace('(','').replace(')','').replace('*','').split()
#        for e in pointsScore:


    def update(self, blocks):
        for matchBet in blocks:
            mKey = matchBet.getKey()
            if mKey in self.liveBets:
                self.liveBets[mKey] = self.liveBets[mKey].merge(matchBet)
            else:
                self.liveBets[mKey] = matchBet
            self.lastUpdate[mKey] = self.counter
        liveBetsNew = dict()
        lastUpdateNew = dict()
        for betId,bet in self.liveBets.items():
            print(bet.getLastScore(), self.isFinalScore(bet.getLastScore()))
            if (self.counter - self.lastUpdate[betId] > 200) or \
               (self.counter - self.lastUpdate[betId] > 10) and self.isFinalScore(bet.getLastScore()):
                self.bets[bet.dt + '\t' + betId] = bet
                print(bet)
            else:
                liveBetsNew[betId] = bet
                lastUpdateNew[betId] = self.lastUpdate[betId]
        self.liveBets = liveBetsNew
        self.lastUpdate = lastUpdateNew
        self.counter += 1
