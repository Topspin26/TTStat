import pandas as pd
import xgboost as xgb
import pickle

from Storages import *
from Entity import *
from common import *

class TTModel:
    def __init__(self, dirname):
        self.matches_columns = ['Дата', 'Время', 'Турнир', 'id1', 'Участник1', 'id2', 'Участник2', 'Счет', 'Очки', 'Источники', 'БК', 'Хеш']
        self.matches_dtypes = ['string'] * 12

        self.bets_columns = ['Дата', 'Время', 'Турнир', 'id1', 'id2', 'Счет', 'К1', 'К2']
        self.bets_dtypes = ['string'] * 8

        self.players_columns = ['id', 'Игрок', 'Матчи']
        self.players_dtypes = ['string'] * 2 + ['number']

        self.player_rankings_columns = ['Дата', 'Источник', 'Рейтинг', 'Ранг']
        self.player_rankings_dtypes = ['string'] * 2 + ['number'] * 2

        self.playersDict = GlobalPlayersDict()

        self.rankingSources = []
        self.rankingSources.append(['ttfr', dirname + '/prepared_data/propingpong/ranking_rus.txt'])
        self.rankingSources.append(['ittf', dirname + '/prepared_data/propingpong/ranking_ittf.txt'])
        self.rankingSources.append(['my', dirname + '/test/all_rankings_mw_fresh.txt'])
        self.rankingSources.append(['liga_pro', dirname + '/prepared_data/liga_pro/ranking_liga_pro.txt'])

        self.rankingStorage = RankingsStorage(self.rankingSources)

        self.rankings_columns = ['#', 'id', 'Игрок'] + [e[0] for e in self.rankingSources]
        self.rankings_dtypes = ['number'] + ['string'] * 2 + ['number'] * len(self.rankingSources)

        self.players = dict()
        #self.playersDict = dict()
        for k,v in sorted(self.playersDict.id2names.items(), key = lambda x: x[0]):
            #self.playersDict[k] = len(self.players)
            self.players[k] = Player(k, v, k[0])

        sources = []
        sources.append(['master_tour', dirname + '/prepared_data/master_tour/all_results.txt'])
        sources.append(['liga_pro', dirname + '/prepared_data/liga_pro/all_results.txt'])
        sources.append(['challenger_series', dirname + '/prepared_data/challenger_series/all_results.txt'])
        sources.append(['bkfon', dirname + '/prepared_data/bkfon/all_results.txt'])
        sources.append(['local', dirname + '/prepared_data/local/kchr_results.txt'])
        sources.append(['ittf', dirname + '/prepared_data/ittf/all_results.txt'])
        sources.append(['rttf', dirname + '/prepared_data/rttf/all_results.txt'])

        self.matchesStorage = MatchesStorage(sources)

        self.matches = self.matchesStorage.matches
        self.hash2matchInd = self.matchesStorage.hash2matchInd
        for match in self.matches:
            for e in match.players[0]:
                self.players[e].matches.append(match)
            for e in match.players[1]:
                self.players[e].matches.append(match)

        self.matchesBetsStorage = MatchesBetsStorage(self.hash2matchInd)
        self.bets = self.matchesBetsStorage.bets

        self.n = len(self.matches)
        '''
        with open(r'D:\Programming\SportPrognoseSystem\TTStat\test\dataset.txt', 'w', encoding = 'utf-8') as fout:
            fout.write('\t'.join(['date', 'time', 'compName', 'players1', 'players2', 'setsScore', 'pointsScore', 'rus1', 'ittf1', 'my1', 'rus2', 'ittf2', 'my2', 'y']) + '\n')
            for match in self.matches:
                if match.date >= '2015':
                    if len(match.players[0]) == 1 and not (match.wins is None):
                        r1 = self.getFeatures(match.players[0][0], match.date)
                        r2 = self.getFeatures(match.players[1][0], match.date)
                        r1 = [str(e) for e in [r1['rus'], r1['ittf'], r1['my']]]
                        r2 = [str(e) for e in [r2['rus'], r2['ittf'], r2['my']]]
                        fout.write('\t'.join(match.toArr() + r1 + r2 + [str(match.wins[0])]) + '\n')

        with open(r'D:\Programming\SportPrognoseSystem\TTStat\test\model_3.pkl', 'rb') as fin:
            self.model = pickle.load(fin)
        '''

    def getHref(self, id, name):
        return '<a href=/players/' + id + '>' + name + '</a>'

    def getPlayerNames(self, id):
        return self.playersDict.getNames(id)
    def getPlayerName(self, id):
        return self.playersDict.getName(id)
    def getMatchPlayersNames(self, ids):
        return [self.playersDict.getName(id) for id in ids]

    def getMatchesTable(self, matches, sortInd = 0, sortAsc = 1):
        data = []
        for i,match in enumerate(matches):
            id1 = ' - '.join(match.players[0])
            names1 = ' - '.join(self.getMatchPlayersNames(match.players[0]))
            id2 = ' - '.join(match.players[1])
            names2 = ' - '.join(self.getMatchPlayersNames(match.players[1]))
            flBet = '+' if match.hash in self.bets else ''
            data.append([match.date, match.time, match.compName, id1, names1, id2, names2, match.setsScore, match.pointsScore, '; '.join(match.sources), flBet, match.hash])
        data = sorted(data, key = lambda x: x[sortInd], reverse = (sortAsc == 0))
        for i,row in enumerate(data):
            names1 = ' - '.join([self.getHref(e, self.playersDict.getName(e)) for e in row[3].split(' - ')])
            names2 = ' - '.join([self.getHref(e, self.playersDict.getName(e)) for e in row[5].split(' - ')])
            data[i][4] = names1
            data[i][6] = names2

        return data

    def getMatchBetsTable(self, matchHash, sortInd = 0, sortAsc = 1):
        data = []
        if not (matchHash in self.bets):
            return data
        matchBet = self.bets[matchHash]
        for i in range(len(matchBet.ts)):
            id1 = ' - '.join(matchBet.players[0])
            id2 = ' - '.join(matchBet.players[1])
            data.append([matchBet.ts[i][:10], matchBet.ts[i][11:], matchBet.compName, id1, id2, matchBet.score[i], str(matchBet.bet_win[0][i]), str(matchBet.bet_win[1][i])])

        return data

    def getPlayersTable(self, players):
        data = []
        for player in players:
            data.append([player.id, self.getHref(player.id, player.name), len(player.matches)])
        return data

    def getFeatures(self, playerId, curDate):
        dt = curDate[:-3]
        myR = self.rankingStorage.getRankings(playerId, 'ttfr', curDate)

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

    def getRankings(self, playerId, curDate, ws = 1):
        #[leftDAte = curDate - ws < date <= curDate]
        myR = self.rankingStorage.getRankings(playerId, 'my', curDate, ws)
        rusR = self.rankingStorage.getRankings(playerId, 'ttfr', curDate, ws)
        ittfR = self.rankingStorage.getRankings(playerId, 'ittf', curDate, ws)
        ligaproR = self.rankingStorage.getRankings(playerId, 'liga_pro', curDate, ws)
        return {'rus': rusR, 'ittf': ittfR, 'my': myR, 'liga_pro': ligaproR}

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
