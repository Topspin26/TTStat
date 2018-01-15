
class Presenter:
    def __init__(self, model):
        self.model = model

        self.matches_columns = ['Дата', 'Турнир', 'Игрок1', 'Игрок2', 'Счет', 'Источники', 'БК', 'Хеш']
        self.matches_dtypes = ['string'] * 8

        self.competitions_columns = ['Дата', 'Название', 'Игроки', 'Матчи', 'Источники']
        self.competitions_dtypes = ['string'] * 2 + ['number'] * 2 + ['string']

        self.bets_columns = ['Дата', 'Турнир', 'id1', 'id2', 'Счет', 'К1', 'К2', 'Тотал', 'Б', 'М']
        self.bets_dtypes = ['string'] * 10

        self.players_columns = ['id', 'Игрок', 'LP', 'Матчи']
        self.players_dtypes = ['string'] * 3 + ['number']

        self.player_rankings_columns = ['Дата', 'Источник', 'Рейтинг', 'Ранг']
        self.player_rankings_dtypes = ['string'] * 2 + ['number'] * 2

        self.rankings_columns = ['#', 'id', 'Игрок'] + [e[0] for e in self.model.rankingSources]
        self.rankings_dtypes = ['number'] + ['string'] * 2 + ['number'] * len(self.model.rankingSources)


    def getHref(self, playerId, playerName, filterFlag=False):
        if (playerId is not None) and playerId != '':
            hr = '<a href=/players/' + playerId + ' target="blank">' + str(playerName) + '</a>'
            if filterFlag:
                return '<a class="matchFilter" playerId="' + playerId + \
                       '"><span class="glyphicon glyphicon-search"></span></a>' + hr
            else:
                return hr
        return str(playerName)

    def getCompHref0(self, id, name):
        return '<a href=/competitions/' + str(id) + ' target="_blank">' + name + '</a>'

    def getCompHref(self, compId, name):
        if compId is not None:
            return '<a class="matchFilter" compId="' + str(compId) + '">' + \
                   '<span class="glyphicon glyphicon-search"></span></a>' + \
                   '<a href=/competitions/' + str(compId) + ' target="_blank">' + name + '</a>'
        return name

    def getSourceHref(self, name):
#        return '<a class="matchFilter" sourceId="' + str(name) + '">' + '<span class="glyphicon glyphicon-search"></span></a>' + \
#               '<a href=/sources/' + str(name) + ' target="blank">' + name + '</a>'
        return '<a class="matchFilter" sourceId="' + str(name) + '">' + \
               '<span class="glyphicon glyphicon-search"></span></a>' + name

    def getPlayersHrefsByIds(self, ids, filterFlag=False):
        return ' - '.join([self.getHref(e, self.model.playersDict.getName(e, fl=1), filterFlag=filterFlag) for e in ids])

    def getPlayersHrefsByIdsNames(self, ids, names, filterFlag=False):
        arr = []
        for e1, e2 in zip(ids, names):
            name = self.model.playersDict.getName(e1, fl=1)
            playerId = e1
            if name is None:
                name = e2
                playerId = None
            arr.append(self.getHref(playerId, name, filterFlag=filterFlag))
        return ' - '.join(arr)

    def getPlayersIdsHrefs(self, players, ids, filterFlag=False):
        arr = []
        for playerName, playerId in zip(players, ids):
            if playerId == '' or playerId.find(',') != -1:
                arr.append(playerName)
            else:
                arr.append(self.getHref(playerId, playerName))
        return ' - '.join(arr)

    def getLiveBetsTable(self):
        data = []
        for key, matchBet in sorted(self.model.betsStorage.liveBets.items(), key=lambda x: x[1].dt, reverse=1):
            names1 = self.getPlayersIdsHrefs(matchBet.names[0], matchBet.ids[0])
            names2 = self.getPlayersIdsHrefs(matchBet.names[1], matchBet.ids[1])
            info = '<br>'.join([str((k, v)) for k, v in sorted(matchBet.eventsInfo[-1][1].items(),
                                                               key=lambda x: '0' if x[0] == 'match' else x[0][0])])
            data.append([matchBet.dt, matchBet.eventsInfo[-1][0],
                         matchBet.eventId, matchBet.compName, str(matchBet.extraInfo),
                         names1, names2, matchBet.getLastScore(),
                         info, matchBet.getKey()])
        return data

    def getBetsTable(self):
        data = []
        for mKey, matchBet in sorted(self.model.betsStorage.bets.items(), key=lambda x: x[1].dt, reverse=1):
            if mKey[0] != 'l':
                names1 = self.getPlayersIdsHrefs(matchBet.names[0], matchBet.ids[0])
                names2 = self.getPlayersIdsHrefs(matchBet.names[1], matchBet.ids[1])
                data.append([matchBet.dt, matchBet.eventsInfo[-1][0],
                             matchBet.eventId, matchBet.compName, str(matchBet.extraInfo),
                             names1, names2, matchBet.getLastScore(),
                             mKey])
        return data

    def getMatchesTable(self, matches, filterFlag=False):
        data = []
        for i, match in enumerate(matches):
            names1 = self.getPlayersHrefsByIdsNames(match.ids[0], match.names[0], filterFlag=filterFlag)
            names2 = self.getPlayersHrefsByIdsNames(match.ids[1], match.names[1], filterFlag=filterFlag)
            flBet = '+' if match.hash in self.model.betsStorage.bets else ''
            data.append([match.date + ', ' + (match.time if match.time else '-'), self.getCompHref(match.compId, match.compName),
                         names1, names2, match.setsScore + ', (' + match.pointsScore + ')',
                         '; '.join([self.getSourceHref(e) for e in match.sources]), flBet, match.hash])
        return data

    def getMatchBetsTable(self, matchHash):
        data = []
        matchBet = self.model.betsStorage.getBet(matchHash)
        if matchBet is None:
            return data
        if matchHash[0] != 'l':
            left, right, step = 0, len(matchBet.eventsInfo), 1
        else:
            left, right, step = len(matchBet.eventsInfo)-1, -1, -1

        id1 = ' - '.join(matchBet.names[0])
        id2 = ' - '.join(matchBet.names[1])
        dt = matchBet.dt
        match = self.model.getMatch(matchHash)
        if match is not None:
            dt = min(dt, match.date + ' ' + (match.time if match.time else ''))
        for i in range(left, right, step):
            try:
                mb = matchBet.eventsInfo[i][1].get('match', dict())
                pWin = self.model.predict(matchBet, dt, score=mb.get('score', None), betInfo=mb)

            except Exception as ex:
                print(ex)
                print(matchBet.eventsInfo[i])
                raise

            data.append([matchBet.eventsInfo[i][0][:10] + ', ' + matchBet.eventsInfo[i][0][11:],
                         matchBet.compName, id1, id2,
                         mb.get('score', ''),
                         str(mb.get('win1', '')) + str(pWin), mb.get('win2', ''),
                         mb.get('total_g', [''])[0], mb.get('total_g', [''])[1:3], mb.get('total_l', [''])[1:3]])

        return data

    def getPlayersTable(self, players):
        data = []
        for player in players:
            href = player.hrefs.get('liga_pro', '')
            if href != '':
                href = '<a href=' + href + ' target="_blank">' + href + '</a>'
            data.append([player.id,
                         self.getHref(player.id, player.name),
                         href,
                         len(player.matches)])
        return data

    def getCompetitionsTable(self, competitions):
        data = []
        for comp in competitions:
            data.append([comp.finishDate, self.getCompHref0(comp.id, comp.name),
                         str(len(comp.playersSet)), str(len(comp.matches)),
                         '; '.join([self.getSourceHref(e) for e in comp.sources])])
        return data
