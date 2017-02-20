import scipy as sp
import scipy.sparse as sps
import numpy as np
import pandas as pd
import xgboost as xgb
import pickle

from Entity import *
from common import *

def readPlayersRankings(filename):
    playersRankings = dict()
    with open(filename, 'r', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            tokens = [e.strip() for e in tokens]
            if not(tokens[1] in playersRankings):
                playersRankings[tokens[1]] = dict()
            playersRankings[tokens[1]][tokens[0]] = tokens[2:]
    return playersRankings


class TTModel:
    def __init__(self):
        self.matches_columns = ['Дата', 'Время', 'Турнир', 'id1', 'Участник1', 'id2', 'Участник2', 'Счет', 'Очки']
        self.matches_dtypes = ['string'] * 9

        self.players_columns = ['id', 'Игрок', 'Матчи']
        self.players_dtypes = ['string'] * 2 + ['number']

        self.rankings_columns = ['Дата', 'Источник', 'Рейтинг', 'Ранг']
        self.rankings_dtypes = ['string'] * 2 + ['number'] * 2

        filenamePlayersMen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_men.txt'
        self.mId = readPlayers(filenamePlayersMen)
        filenamePlayersWomen = r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_women.txt'
        self.wId = readPlayers(filenamePlayersWomen)
        self.mwId = dict(list(self.mId.items()) + list(self.wId.items()))

        self.rusRankings = readPlayersRankings('prepared_data/propingpong/ranking_rus.txt')
        self.ittfRankings = readPlayersRankings('prepared_data/propingpong/ranking_ittf.txt')
        self.myRankings = readPlayersRankings('test/all_rankings_mw.txt')

        self.players = []
        self.playersDict = dict()
        for k,v in sorted(self.mId.items(), key = lambda x: x[0]):
            self.playersDict[k] = len(self.players)
            self.players.append(Player(k, v, 'm'))
        for k,v in sorted(self.wId.items(), key = lambda x: x[0]):
            self.playersDict[k] = len(self.players)
            self.players.append(Player(k, v, 'w'))

        filenames = []
        filenames.append(r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\master_tour\all_results.txt')
        filenames.append(r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\bkfon\all_results.txt')
        filenames.append(r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\ittf\all_results.txt')
        self.matches = []

        matchesSet = set()
        for filename in filenames:
            print(filename)
            with open(filename, encoding='utf-8') as fin:
                headerTokens = next(fin).strip().split('\t')
                headerDict = dict(zip(headerTokens, range(len(headerTokens))))
                lastId = None
                for line in fin:
                    tokens = line.split('\t')
                    #id1 = [self.mwId[e] for e in tokens[headerDict['id1']].split(';')]
                    #id2 = [self.mwId[e] for e in tokens[headerDict['id2']].split(';')]
                    match = Match(tokens[headerDict['date']],
                                  [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')],
                                  setsScore=tokens[headerDict['setsScore']],
                                  pointsScore=tokens[headerDict['pointsScore']],
                                  time=tokens[headerDict['time']],
                                  compName=tokens[headerDict['compName']])
                    matchStr = ';'.join([match.date[:7], ' '.join(match.players[0]), ' '.join(match.players[1]), match.setsScore.strip(';'), match.pointsScore.strip(';')])
#                    matchStr = ';'.join([' '.join(match.players[0]), ' '.join(match.players[1]), match.setsScore, match.pointsScore])
                    if not (matchStr in matchesSet) and match.date >= '2014':
                        matchesSet.add(matchStr)
                        self.matches.append(match)
    #                    print(line)
                        for e in tokens[headerDict['id1']].split(';'):
                            self.players[self.playersDict[e]].matches.append(match)
                        for e in tokens[headerDict['id2']].split(';'):
                            self.players[self.playersDict[e]].matches.append(match)
        self.n = len(self.matches)
        with open(r'D:\Programming\SportPrognoseSystem\BetsWinner\test\dataset.txt', 'w', encoding = 'utf-8') as fout:
            fout.write('\t'.join(['date', 'time', 'compName', 'players1', 'players2', 'setsScore', 'pointsScore', 'rus1', 'ittf1', 'my1', 'rus2', 'ittf2', 'my2', 'y']) + '\n')
            for match in self.matches:
                if match.date >= '2015':
                    if len(match.players[0]) == 1 and not (match.wins is None):
                        r1 = self.getFeatures(match.players[0][0], match.date)
                        r2 = self.getFeatures(match.players[1][0], match.date)
                        r1 = [str(e) for e in [r1['rus'], r1['ittf'], r1['my']]]
                        r2 = [str(e) for e in [r2['rus'], r2['ittf'], r2['my']]]
                        fout.write('\t'.join(match.toArr() + r1 + r2 + [str(match.wins[0])]) + '\n')

        with open(r'D:\Programming\SportPrognoseSystem\BetsWinner\test\model_3.pkl', 'rb') as fin:
            self.model = pickle.load(fin)

    def getHref(self, id, name):
        return '<a href=/players/' + id + '>' + name + '</a>'

    def getNames(self, players):
        return [self.mwId.get(e, e) for e in players]

    def getMatchesTable(self, matches, sortInd = 0, sortAsc = 1):
        data = []
        for match in matches:
            id1 = ' - '.join(match.players[0])
            names1 = ' - '.join(self.getNames(match.players[0]))
            id2 = ' - '.join(match.players[1])
            names2 = ' - '.join(self.getNames(match.players[1]))
            data.append([match.date, match.time, match.compName, id1, names1, id2, names2, match.setsScore, match.pointsScore])
        data = sorted(data, key = lambda x: x[sortInd], reverse = (sortAsc == 0))
        for i,row in enumerate(data):
            names1 = ' - '.join([self.getHref(e, self.mwId.get(e, e)) for e in row[3].split(' - ')])
            names2 = ' - '.join([self.getHref(e, self.mwId.get(e, e)) for e in row[5].split(' - ')])
            data[i][4] = names1
            data[i][6] = names2

        return data
        #self.m = 100
        #self.id = np.array(list(range(self.n)))
        #self.name = ['name_' + str(i) for i in range(self.n)]
        #k = 100000
        #np.random.seed(777)
        #data = np.random.randint(2, size = k)
        #row = np.random.randint(self.n, size = k)
        #col = np.random.randint(self.m, size = k)
        #self.y = sps.csc_matrix((data, (row, col)), shape=(self.n, self.m))
        #print(self.n)
        #ys = self.y.sum(axis=1)
        #print(ys[0, 0])


    def getPlayersTable(self, players):
        data = []
        for player in players:
            data.append([player.id, self.getHref(player.id, player.name), len(player.matches)])
        return data

    def getFeatures(self, playerId, curDate):
        dt = curDate[:-3]
        myR = -1
        if playerId in self.myRankings:
            myR = self.myRankings[playerId].get(dt, [-1])[0]
            if myR == '-100':
                myR = -1
        rusR = -1
        if playerId in self.rusRankings:
            rusR = self.rusRankings[playerId].get(dt, [-1])[0]
        ittfR = -1
        if playerId in self.ittfRankings:
            ittfR = self.ittfRankings[playerId].get(dt, [-1])[0]
        return {'rus': rusR, 'ittf': ittfR, 'my': myR}

    def makePrediction(self, playerId1, playerId2):
        r1 = self.getFeatures(playerId1, '2017-01-30')
        r2 = self.getFeatures(playerId2, '2017-01-30')
        r1 = [float(e) for e in [r1['rus'], r1['ittf'], r1['my']]]
        r2 = [float(e) for e in [r2['rus'], r2['ittf'], r2['my']]]
        ff = [[r1[0] - r2[0], r1[1] - r2[1], r1[2] - r2[2]]]
        print(ff)
        df1 = pd.DataFrame(index=[0], data=ff, columns=['drus', 'dittf', 'dmy'])
        df2 = -df1
        p1 = self.model.predict_proba(df1)[0, 1]
        p2 = self.model.predict_proba(df2)[0, 0]
        print([p1, p2])
        print(r1)
        print(r2)
        if (r1[0] != -1) and (r2[0] != -1) and (r1[2] != -1) and (r2[2] != -1):
            return format((p1 + p2) / 2 * 100, '.1f') + '%'
        return '?'
