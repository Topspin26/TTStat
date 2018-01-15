from Storages import *
from BetsStorage import *
from Entity import *
from common import *


class TTModel:
    def __init__(self, dirname):

        self.playersDict = GlobalPlayersDict(mode='filtered', dirname=dirname + '/')

        self.rankingSources = []
        self.rankingSources.append(['ttfr', dirname + '/prepared_data/propingpong/ranking_rus.txt'])
        self.rankingSources.append(['ittf', dirname + '/prepared_data/propingpong/ranking_ittf.txt'])
        #self.rankingSources.append(['my', dirname + '/prepared_data/rankings/all_rankings_mw_fresh_sets_1.txt'])

        for ws in [730]:
            for matchesCntBorder in [4]:
                # for ws in [365, 730]:
                #    for matchesCntBorder in [1, 4]:
                self.rankingSources.append(['ranking_my_' + str(ws) + '_' + str(matchesCntBorder),
                                       ['prepared_data/rankings/rankings_m_sets_sources=0_ws=' + str(
                                           ws) + '_matchesCntBorder=' + str(matchesCntBorder) + '.txt',
                                        'prepared_data/rankings/rankings_w_sets_sources=0_ws=' + str(
                                            ws) + '_matchesCntBorder=' + str(matchesCntBorder) + '.txt']])

        self.rankingSources.append(['liga_pro', dirname + '/prepared_data/liga_pro/ranking_liga_pro.txt'])

        self.rankingsStorage = RankingsStorage(self.rankingSources)

        for ws in [730]:
            for matchesCntBorder in [4]:
                rName = 'my_' + str(ws) + '_' + str(matchesCntBorder)
                self.rankingsStorage.readPlayersDayRankings('ranking_' + rName + '_day', 'test/dayRankings_m_' + rName + '.txt')
                self.rankingsStorage.readPlayersDayRankings('ranking_' + rName + '_day', 'test/dayRankings_w_' + rName + '.txt')


        self.players = dict()
        #self.playersDict = dict()
        for k, v in sorted(self.playersDict.id2names.items(), key=lambda x: x[0]):
            #self.playersDict[k] = len(self.players)
            self.players[k] = Player(k, v, k[0])

        with open(dirname + '/prepared_data/liga_pro/players_liga_pro.txt', encoding='utf-8') as fin:
            for line in fin:
                tokens = line.strip().split('\t')
                self.players[tokens[0]].addHref('liga_pro', tokens[2])

        sources = list()
        sources.append(['master_tour', dirname + '/prepared_data/master_tour/all_results.txt'])
        sources.append(['liga_pro', dirname + '/prepared_data/liga_pro/all_results.txt'])
        sources.append(['challenger_series', dirname + '/prepared_data/challenger_series/all_results.txt'])
        sources.append(['bkfon', dirname + '/prepared_data/bkfon/all_results.txt'])
        sources.append(['local', dirname + '/prepared_data/local/kchr_results.txt'])
        sources.append(['ittf', dirname + '/prepared_data/ittf/all_results.txt'])
        sources.append(['rttf', dirname + '/prepared_data/rttf/all_results.txt'])

        self.matchesStorage = MatchesStorage(sources)
        self.sortMatches()

        self.competitionsStorage = CompetitionsStorage()
        for match in self.matches:
            compId = self.competitionsStorage.getCompId(match.compName)
            match.setCompId(compId)
            self.competitionsStorage.getComp(compId).addMatch(match)

        for match in self.matches:
            for i in range(2):
                for e in match.ids[i]:
                    if e not in {'-', '?'}:
                        self.players[e].matches.append(match)

        self.betsStorage = BetsStorage()
        self.betsStorage.loadFromFile(dirname + '/prepared_data/bkfon/live/tail.txt')
        # self.betsStorage.loadFromFile(dirname + '/prepared_data/bkfon/live/all_bets_prepared.txt')
#        self.matchesBetsStorage = MatchesBetsStorage(self.hash2matchInd,filename=)

#        self.bets = self.betsStorage.bets

        self.lastUpdateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10] + ' 00:00:00'
        self.lastUpdateTime = '2017-06-12 13:53:00'

        self.n = len(self.matches)
        '''
        with open(r'D:\Programming\SportPrognoseSystem\TTStat\test\model_3.pkl', 'rb') as fin:
            self.model = pickle.load(fin)
        '''

        self.predictionMachine = None

    def setPredictionMachine(self, predictionMachine):
        self.predictionMachine = predictionMachine
        self.predictionMachine.setRankingsStorage(self.rankingsStorage)
        self.predictionMachine.setMatchesStorage(self.matchesStorage)

    def sortMatches(self):
        self.matchesStorage.matches = list(sorted(self.matchesStorage.matches,
                                                  key=lambda x: x.date + ', ' + (x.time if x.time else '-'), reverse=1))
        self.matches = self.matchesStorage.matches
        self.matchesStorage.buildHash2MatchInd()
        self.hash2matchInd = self.matchesStorage.hash2matchInd

    def addMatch(self, source, match):
        if match.compName.find('TT-CUP') != -1:
            return
        # print('models.addMatch', match.hash)
        isNew = self.matchesStorage.addMatch(source, match)
        if isNew is True:
            for i in range(2):
                for e in match.ids[i]:
                    if e in self.players:
                        self.players[e].matches.append(match)
                        self.players[e].matches = list(sorted(self.players[e].matches,
                                                              key=lambda x: x.date + ', ' + (x.time if x.time else '-'), reverse=1))

        self.rankingsStorage.addMatch(source, match)

    def update(self, rows):
        lastTime = None
        block = []
        rowNames = dict(zip(['id', 'datetime', 'eventId', 'compName', 'info'], range(5)))
        isFinished = False
        for row in rows:
            row = [str(e) for e in row]
            # print(row)
            curTime = str(row[1])
            if lastTime is not None and curTime != lastTime:
                finished = self.betsStorage.update(block)
                for finishedMatch in finished:
                    print('FINISHED')
                    print(finishedMatch.toStr())
                    self.addMatch('bkfon_live', finishedMatch)
                    isFinished = True
                block = []
            tokens = row[rowNames['info']].split('\t')
            dt = row[rowNames['datetime']]
            eventsInfo = json.loads(tokens[2])
            # Старый формат в базе
            if len(eventsInfo) > 1:
                eventsInfo = [eventsInfo]
            names = [tokens[0].split(';'), tokens[1].split(';')]
            extraInfo = dict()
            score = eventsInfo[0][1]['match']['score']
            if names[0][0].startswith('Game'):
                try:
                    names = [e.strip().split('\\') for e in score.split(')')[1].split('-')]
                    assert len(names) == 2
                    extraInfo['teams'] = [tokens[0].replace('Game', '').strip()[1:].strip().split(';'), tokens[1].strip().split(';')]
                    extraInfo['game'] = tokens[0].replace('Game', '').strip()[0]
                except:
                    names = [tokens[0].split(';'), tokens[1].split(';')]
                    print('ERROR_SCORE', eventsInfo)
            else:
                try:
                    extraInfo['round'] = score.split(')')[1].strip()
                    if extraInfo['round'] == '':
                        extraInfo.pop('round')
                except:
                    pass
            ids = self.getMatchPlayersIds(names, compName=row[rowNames['compName']], date=dt[:10])
            block.append(MatchBet(row[rowNames['eventId']], dt, row[rowNames['compName']],
                                  ids, eventsInfo, names=names, extraInfo=extraInfo))
            self.lastUpdateTime = max(self.lastUpdateTime, curTime)
            lastTime = curTime
        if lastTime is not None:
            finished = self.betsStorage.update(block)
            for finishedMatch in finished:
                print('FINISHED')
                print(finishedMatch.toStr())
                self.addMatch('bkfon_live', finishedMatch)
                isFinished = True

        if isFinished is True:
            self.sortMatches()

        print(self.lastUpdateTime)

    def getPlayerNames(self, playerId):
        return self.playersDict.getNames(playerId)

    def getPlayerName(self, playerId):
        return self.playersDict.getName(playerId)

    def getMatchPlayersNames(self, ids):
        return [self.playersDict.getName(id) for id in ids]

    def getMatchPlayersIds(self, players, compName=None, date=None):
        # for i in range(2):
        #    for playerName in players[i]:
        #        playerIds = self.playersDict.getId(playerName)

        ids = [[], []]
        for i in range(2):
            for player in players[i]:
                player = ' '.join(player.split()).strip()
                playerId = self.playersDict.getId(player)
                if len(playerId) == 1:
                    pass
                elif len(playerId) > 1:
                    if compName is not None and date is not None:
                        idGood = []
                        source = 'bkfon'
                        if compName.find('Мастер-Тур') != -1:
                            source = 'master_tour'
                        elif compName.find('Лига Про') != -1:
                            source = 'liga_pro'

                        for e in playerId:
                            if self.matchesStorage.isActive(e, source, date):
                                idGood.append(e)
                        if len(idGood) == 1:
                            playerId = idGood
                ids[i].append(','.join(playerId))

        return ids

    def getMatch(self, matchId):
        if matchId in self.hash2matchInd:
            return self.matches[self.hash2matchInd[matchId]]
        elif matchId in self.betsStorage.bets:
            return self.betsStorage.bets[matchId].getMatch()
        return None

    def getLiveBet(self, matchId):
        return self.betsStorage.getBet(matchId)
        return None

    def getFeatures(self, matchBet, dt):
        mb = dict()
        if matchBet is None:
            return dict()
        if len(matchBet.eventsInfo) != 0:
            mb = matchBet.eventsInfo[0][1].get('match', dict())
        allFeatures = \
            self.predictionMachine.getFeatures(
                matchBet.getMatch(),
                dt,
                score=None,
                betInfo=mb
            )
        return allFeatures

    def predict(self, matchBet, dt, score=None, betInfo=None):
        pWin = \
            self.predictionMachine.predict(
                matchBet.getMatch(),
                dt,
                score=score,
                betInfo=betInfo
            )
        return pWin

    def getRankings(self, playerId, curDate, ws=1):
        return self.rankingsStorage.getRankings(playerId, curDate, ws=ws)

    def makePrediction(self, playerId1, playerId2):
        # r1 = self.getFeatures(playerId1, datetime.datetime.now().strftime("%Y-%m-%d"))
        # r2 = self.getFeatures(playerId2, datetime.datetime.now().strftime("%Y-%m-%d"))
        # r1 = [float(e) for e in [r1['liga_pro'], r1['my']]]
        # r2 = [float(e) for e in [r2['liga_pro'], r2['my']]]
        # ff = [[r1[0] - r2[0], r1[1] - r2[1]]]
        # if r1[0] == -1 or r2[0] == -1:
        #     ff[0][0] = 0
        # if r1[1] == -1 or r2[1] == -1:
        #     ff[0][1] = 0
        # print(ff)
        # self.model = linear_model.LogisticRegression(fit_intercept=False)
        # self.model.coef_ = np.array([[ 0.00957611, 0.10476427]])
        # self.model.intercept_ = 0
        # '''
        # df1 = pd.DataFrame(index=[0], data=ff, columns=['drus', 'dittf', 'dmy'])
        # df2 = -df1
        # '''
        # print(self.model.predict_proba(ff))
        # p1 = self.model.predict_proba(ff)[0, 1]
        # p2 = p1
        # #p2 = self.model.predict_proba(-ff)[0, 0]
        # print([p1, p2])
        # print(r1)
        # print(r2)
        # if ff[0] != 0 or ff[1] != 0:
        #     return format((p1 + p2) / 2 * 100, '.1f') + '%, <br>' + 'ставка на игрока 1 от кф ' + format(1 / p1, '.2f') + '; <br>' + 'ставка на игрока 2 от кф ' + format(1 / (1 - p1), '.2f') + ';'
        return '?'
