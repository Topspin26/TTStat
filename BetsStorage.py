import json
import copy
import datetime

from Entity import *

class BetsStorage:
    def __init__(self):
        self.bets = dict()
        self.liveBets = dict()
        self.live2bets = dict()
        self.lastUpdate = dict()
        self.counter = 0

    def loadFromFile(self, filename, isPrepared=1):
        with open(filename, encoding='utf-8') as fin:
            for line in fin:
                tokens = line.rstrip('\n').split('\t')
                if isPrepared == 0:
                    eventId = tokens[0]
                    dt = tokens[1]
                    compName = tokens[2]
                    ids = None
                    names = [tokens[3].split(';'), tokens[4].split(';')]
                    info = json.loads(tokens[5])
                    self.update([MatchBet(eventId, dt, compName, None, info, names=names)])
                    continue

                eventId = tokens[1]
                dt = tokens[2]
                compName = tokens[3]
                ids = [tokens[4].split(';'), tokens[5].split(';')]
                names = [tokens[6].split(';'), tokens[7].split(';')]
                info = json.loads(tokens[8])


                matchBet = MatchBet(eventId, dt, compName, ids, info, names=names)
                match = matchBet.buildMatch()
                setsScore, pointsScore = match.setsScore, match.pointsScore

                if tokens[-1] != '':
                    pointsScoreFinal = tokens[-1] + ';'
                    setsScoreFinal = tokens[-2]
                    if pointsScore and pointsScoreFinal != pointsScore or setsScore != '' and setsScore != setsScoreFinal:
                        print(dt, compName, ids, setsScore, pointsScore, setsScoreFinal, pointsScoreFinal)
                        info.append(['final', {'match': {'score': setsScoreFinal + ' ' + pointsScoreFinal}}])

                        matchBet.match.setsScore = setsScoreFinal
                        matchBet.match.pointsScore = pointsScoreFinal
                        match = matchBet.getMatch()

                if setsScore != '':
                    matchHash = match.getHash()

                    if matchHash not in self.bets:
                        self.bets[matchHash] = matchBet
                    else:
                        print('not unique bet match hash')
                        print([dt] + ids[0] + ids[1] + [match.setsScore])

    def update(self, blocks):
        finished = []
        for matchBet in blocks:
            mKey = matchBet.getKey()
            if mKey in self.liveBets:
                self.liveBets[mKey] = self.liveBets[mKey].merge(matchBet)
            else:
                isMerge = False
                for mCurKey in list(self.liveBets.keys()):
                    curBet = self.liveBets[mCurKey]
                    if curBet.checkOnMerge(matchBet):

                        print(self.liveBets.keys(), mKey)
                        print('potential merge\n' +
                              matchBet.getLastScore() + ' ' + str(matchBet) + '\n' +
                              curBet.getLastScore() + ' ' + str(curBet) + '\n')

                        curBet = curBet.merge(matchBet, isSplitEvent=False)
                        self.liveBets[mKey] = curBet
                        self.liveBets.pop(mCurKey)
                        isMerge = True

                if isMerge is False:
                    self.liveBets[mKey] = matchBet
            self.lastUpdate[mKey] = self.counter
        liveBetsNew = dict()
        lastUpdateNew = dict()
        for mKey, bet in self.liveBets.items():
            #print(bet.getLastScore(), self.isFinalScore(bet.getLastScore()))
            if (self.counter - self.lastUpdate[mKey] > 200) or \
               (self.counter - self.lastUpdate[mKey] > 10) and MatchBet.isFinalScore(bet.getLastScore()):

                self.bets[mKey] = bet
                # ids = [[''] * len(bet.names[0]), [''] * len(bet.names[0])]
                # if bet.ids is not None:
                #     ids = copy.deepcopy(bet.ids)
                bet.buildMatch()
                match = bet.getMatch()
                # setsScore, pointsScore = MatchBet.parseScore(bet.getLastScore(), isParsed=False)
                self.bets[match.hash] = bet
                finished.append(match)
                self.live2bets[mKey] = match.hash
            else:
                liveBetsNew[mKey] = bet
                lastUpdateNew[mKey] = self.lastUpdate[mKey]
        self.liveBets = liveBetsNew
        self.lastUpdate = lastUpdateNew
        self.counter += 1

        return finished

    def getBet(self, matchHash):
        if matchHash[0] == 'l' and matchHash not in self.live2bets:
            return self.liveBets.get(matchHash, None)
        return self.bets.get(self.live2bets.get(matchHash, matchHash), None)
