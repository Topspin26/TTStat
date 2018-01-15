from flask import render_template, request, flash, redirect
from ttstat import ttstat, ttModel, db, ttPresenter
import json


@ttstat.route('/')
@ttstat.route('/index')
def index():
    return render_template('index.html')


@ttstat.route('/matches')
def matches():
    filters = dict()
    filters['compId'] = request.args.get('compId')
    filters['compName'] = ttModel.competitionsStorage.getCompName(request.args.get('compId'))
    filters['playerId'] = request.args.get('playerId')
    filters['sourceId'] = request.args.get('sourceId')
    filters['sourceName'] = request.args.get('sourceId')
    if filters['playerId']:
        filters['playerName'] = ttModel.getPlayerName(request.args.get('playerId'))
    else:
        filters['playerName'] = None
    return render_template('matches.html',
                           matches_columns=ttPresenter.matches_columns,
                           bets_columns=ttPresenter.bets_columns,
                           filters=filters)


@ttstat.route('/matches/<matchId>')
def match_info(matchId):
    filters = dict()
    match = ttModel.getMatch(matchId).toDict()
    match['players'] = [ttPresenter.getPlayersHrefsByIdsNames(e1, e2) for e1, e2 in zip(match['ids'], match['names'])]

    matchBet = ttModel.getLiveBet(matchId)
    dt = match['date'] + ' ' + (match['time'] if match['time'] else '')
    if matchBet is not None:
        dt = min(dt, matchBet.dt)
    allFeatures = ttModel.getFeatures(matchBet, dt)
    # match['hash'] = match['key']
    match['features'] = allFeatures

    return render_template('match_info.html', bets_columns=ttPresenter.bets_columns, match=match, filters=filters)


@ttstat.route('/players')
def players():
    return render_template('players.html', columns=ttPresenter.players_columns)


@ttstat.route('/players/<playerId>')
def player_info(playerId):
    filters = dict()
    filters['compId'] = request.args.get('compId')
    filters['compName'] = ttModel.competitionsStorage.getCompName(request.args.get('compId'))
    filters['playerId'] = request.args.get('playerId')
    filters['sourceId'] = request.args.get('sourceId')
    filters['sourceName'] = request.args.get('sourceId')
    if filters['playerId']:
        filters['playerName'] = ttModel.getPlayerName(request.args.get('playerId'))
    else:
        filters['playerName'] = None
    return render_template('player_info.html', playerId=playerId, name=ttModel.getPlayerNames(playerId),
                           matches_columns=ttPresenter.matches_columns,
                           rankings_columns=ttPresenter.player_rankings_columns,
                           bets_columns=ttPresenter.bets_columns, filters=filters)


@ttstat.route('/competitions')
def competitions():
    filters = dict()
    filters['sourceId'] = request.args.get('sourceId')
    filters['sourceName'] = request.args.get('sourceId')
#    if request.args.get('compId'):
#    filters['compId'] = request.args.get('compId')
#    filters['compName'] = ttModel.competitionsStorage.getCompName(request.args.get('compId'))
    return render_template('competitions.html', competitions_columns=ttPresenter.competitions_columns, filters=filters)


@ttstat.route('/competitions/<compId>')
def competition_info(compId):
    filters = dict()
    filters['compId'] = compId
    filters['compName'] = ttModel.competitionsStorage.getCompName(filters['compId'])
    return render_template('competitions.html', matches_columns=ttPresenter.matches_columns, bets_columns=ttPresenter.bets_columns, filters=filters)


@ttstat.route('/rankings')
def rankings():
    return render_template('rankings.html', columns=ttPresenter.rankings_columns, sex='men')


@ttstat.route('/sources')
def sources():
    return render_template('sources.html')


@ttstat.route('/sources/<sourceId>')
def source_info(sourceId):
    return render_template('sources.html')


@ttstat.route('/rankings/<sex>')
def rankings1(sex):
    return render_template('rankings.html', columns=ttPresenter.rankings_columns, sex=sex)


@ttstat.route('/prognosis')
def prognosis():
    return render_template('prognosis.html', columns=ttPresenter.players_columns)


@ttstat.route('/live')
def live():
    return render_template('live.html',
                           live_columns=['Время старта', 'Время обновления',
                                         'Id события', 'Соревнование', 'Доп. информация',
                                         'Игрок1', 'Игрок2', 'Счет', 'Ставки'],
                           live_finished_columns=['Время старта', 'Время окончания',
                                                  'Id события', 'Соревнование', 'Доп. информация',
                                                  'Игрок1', 'Игрок2', 'Счет'])


@ttstat.route('/live/<matchId>')
def live_match_info(matchId):
    filters = dict()
    matchBet = ttModel.getLiveBet(matchId)
    match = matchBet.toDict()
    allFeatures = ttModel.getFeatures(matchBet, matchBet.dt)
    match['players'] = [ttPresenter.getPlayersHrefsByIdsNames(e1, e2) for e1, e2 in zip(match['ids'], match['names'])]
    match['hash'] = match['key']
    match['features'] = allFeatures
    return render_template('live_match_info.html', bets_columns=ttPresenter.bets_columns, match=match, filters=filters)


@ttstat.route("/_retrieve_live_data")
def retrieve_live_data():
#    cur = db.cursor()
#    cur.execute("SELECT * FROM fonbet_live WHERE datetime = (SELECT MAX(datetime) FROM fonbet_live)")
#    db.commit()
    aaData_rows = ttPresenter.getLiveBetsTable()
#    for row in cur.fetchall():
#        aaData_rows.append([str(e) for e in row])

#    text = request.values['sSearch'].lower()
#    print(text)

    output = dict()
    output['iTotalRecords'] = str(len(aaData_rows))
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    output['iTotalDisplayRecords'] = str(len(aaData_rows))

    output['aaData'] = aaData_rows
    results = output
    return json.dumps(results)


@ttstat.route("/_retrieve_live_finished_data")
def retrieve_live_finished_data():
    aaData_rows = ttPresenter.getBetsTable()
    #print(aaData_rows)
    output = dict()
    output['iTotalRecords'] = str(len(aaData_rows))
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    output['iTotalDisplayRecords'] = str(len(aaData_rows))

    output['aaData'] = aaData_rows
    results = output
    return json.dumps(results)


@ttstat.route('/selectPlayer', methods=['POST'])
def selectPlayer():
    playerId = request.values['playerId']
    print(playerId)
    res = dict()
    res['status'] = 'OK'
    res['playerId'] = playerId
    res['playerName'] = ttModel.getPlayerName(playerId)
    res['playerR'] = str(ttModel.getFeatures(playerId))
    return json.dumps(res)


@ttstat.route('/makePrognosis', methods=['POST'])
def makePrognosis():
    playerId1 = request.values['playerId1']
    playerId2 = request.values['playerId2']
    print([playerId1, playerId2])
    res = dict()
    res['status'] = 'OK'

    res['pred'] = ttModel.makePrediction(playerId1, playerId2)
    print(res['pred'])
    return json.dumps(res)


@ttstat.route("/_retrieve_players_names")
def get_players_names():
    s = request.values['name']
    res = []
    for k,player in sorted(ttModel.players.items(), key=lambda x: x[1].name):
        if player.findString(s) is True:
            res.append('{"name": "' + player.name + '","id": "' + player.id + '"}')
            if len(res) > 10:
                break
    print('[' + ','.join(res) + ']')
    return '[' + ','.join(res) + ']'


@ttstat.route("/_retrieve_matches_data")
def get_matches_data():
    player0IdFilter = None
    if 'player0Id' in request.values:
        player0IdFilter = request.values['player0Id']
    print(player0IdFilter)

    playerIdFilter = None
    if 'playerId' in request.values:
        playerIdFilter = request.values['playerId']
    print(playerIdFilter)

    compIdFilter = None
    if 'compId' in request.values:
        compIdFilter = request.values['compId']
    print('compId', compIdFilter)

    print(request.values)
    print(request.values['sSortDir_0'])
    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
    output['sEcho'] = str(int(request.values['sEcho']))

    sourceIdFilter = None
    if 'sourceId' in request.values:
         sourceIdFilter = request.values['sourceId']
    #print(sources)

    text = request.values['sSearch'].lower()
    print(text)
    aaData_rows = []
    c = 0
    #ys = td.y.sum(axis=1)

    matches = []
    matchesList = ttModel.matches
    if player0IdFilter is not None:
        matchesList = ttModel.players[player0IdFilter].matches
    elif compIdFilter is not None:
        matchesList = ttModel.competitionsStorage.getComp(compIdFilter).matches
    output['iTotalRecords'] = str(len(matchesList))
    if playerIdFilter or player0IdFilter or compIdFilter or sourceIdFilter or text != '':
        for match in matchesList:
            if compIdFilter:
                if str(match.compId) != str(compIdFilter):
                    continue
            if sourceIdFilter and sourceIdFilter not in match.sources:
                continue
            flMatch = 0
            for i in range(2):
                for playerId, playerName in zip(match.ids[i], match.names[i]):
                    if playerId not in {'', '-', '?'}:
                        for plId in playerId.split(','):
                            if plId != player0IdFilter:
                                if ttModel.players[plId].findString(text) is True:
                                    flMatch = 1
                    else:
                        if playerName.lower().find(text.lower()) != -1:
                            flMatch = 1
    #        if (' - '.join(ttModel.getNames(match.ids[0]))).lower().find(text) != -1 or (' - '.join(ttModel.getNames(match.ids[1]))).lower().find(text) != -1:
            if request.values['playerInfo'] == '1' and player0IdFilter not in match.ids[0]:
                match = match.reverse()
            if player0IdFilter:
                if playerIdFilter and playerIdFilter not in match.ids[1]:
                    continue
            else:
                if playerIdFilter and playerIdFilter not in (match.ids[0] + match.ids[1]):
                    continue
            if flMatch == 1:
                matches.append(match)
                c += 1
    else:
        print('NO filters')
        matches = matchesList
        c = len(matches)
#    sortInd = int(request.values['iSortCol_0'])
#    sortAsc = request.values['sSortDir_0']
#    print([sortInd, ttModel.matches_dtypes[sortInd]])
    aaData_rows = ttPresenter.getMatchesTable(matches[leftInd:rightInd], filterFlag=True)

#    if ttModel.matches_dtypes[sortInd] == 'string':
#        aaData_rows = sorted(aaData_rows, key = lambda x: x[sortInd], reverse=(sortAsc!='asc'))
#    else:
#        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows

    results = output
    return json.dumps(results)


@ttstat.route("/_retrieve_match_bets_data")
def get_match_bets_data():
    print(request.values)
    print(request.values['sSortDir_0'])
    #leftInd = int(request.values['iDisplayStart'])
    #rightInd = leftInd + int(request.values['iDisplayLength'])
    output = dict()
    output['sEcho'] = str(int(request.values['sEcho']))

    #text = request.values['sSearch'].lower()
    #print(text)
    aaData_rows = []
    #ys = td.y.sum(axis=1)

    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
#    print([sortInd, ttModel.matches_dtypes[sortInd]])
    matchHash = request.values['matchHash']
    print(matchHash)
    aaData_rows = ttPresenter.getMatchBetsTable(matchHash)

    c = len(aaData_rows)
    output['iTotalRecords'] = str(c)
    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows#[leftInd:rightInd]

    results = output
    return json.dumps(results)


@ttstat.route("/_retrieve_player_rankings_data")
def get_player_rankings_data():
    playerIdFilter = None
    if 'playerId' in request.values:
        playerIdFilter = request.values['playerId']
    print(playerIdFilter)

    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = dict()
    output['sEcho'] = str(int(request.values['sEcho']))

    c = 0
    output['iTotalRecords'] = 0
    aaData_rows = []
    if playerIdFilter in ttModel.rankingsStorage.rankings['ttfr']:
        output['iTotalRecords'] += len(ttModel.rankingsStorage.rankings['ttfr'][playerIdFilter])
        for e in sorted(ttModel.rankingsStorage.rankings['ttfr'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'TTFR', e[1][0], e[1][1]])
            c += 1
    if playerIdFilter in ttModel.rankingsStorage.rankings['ittf']:
        output['iTotalRecords'] += len(ttModel.rankingsStorage.rankings['ittf'][playerIdFilter])
        for e in sorted(ttModel.rankingsStorage.rankings['ittf'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'ITTF', e[1][0], e[1][1]])
            c += 1
    if playerIdFilter in ttModel.rankingsStorage.rankings['ranking_my_730_4']:
        output['iTotalRecords'] += len(ttModel.rankingsStorage.rankings['ranking_my_730_4'][playerIdFilter])
        for e in sorted(ttModel.rankingsStorage.rankings['ranking_my_730_4'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'MY', format(float(e[1][0]),'.3f'), e[1][1]])
            c += 1
    if playerIdFilter in ttModel.rankingsStorage.rankings['liga_pro']:
        output['iTotalRecords'] += len(ttModel.rankingsStorage.rankings['liga_pro'][playerIdFilter])
        for e in sorted(ttModel.rankingsStorage.rankings['liga_pro'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'LIGA-PRO', e[1][0], 0])
            c += 1
    output['iTotalRecords'] = str(output['iTotalRecords'])
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttPresenter.player_rankings_dtypes[sortInd] == 'string':
        aaData_rows = sorted(aaData_rows, key=lambda x: x[sortInd], reverse=(sortAsc != 'asc'))
    else:
        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows[leftInd:rightInd]
    results = output
    return json.dumps(results)


@ttstat.route("/_retrieve_rankings_data")
def get_rankings_data():
    print(request.values)

    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = dict()
    output['sEcho'] = str(int(request.values['sEcho']))

    text = request.values['sSearch'].lower()
    print(text)

    mw = request.values['rankingsSex'][0]

    dt = request.values['rankingDate']

    c = 0
    total = 0
    aaData_rows = []
    for k,player in ttModel.players.items():
        if player.mw == mw:
            if player.findString(text) is True:
                r = ttModel.getRankings(player.id, dt, 100)
                aaData_rows.append(['0', player.id, player.name, r['ttfr'], r['ittf'], format(float(r['ranking_my_730_4']),'.3f'), r['liga_pro']])
                c += 1
            total += 1
    output['iTotalRecords'] = str(total)

    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttPresenter.rankings_dtypes[sortInd] == 'string':
        aaData_rows = sorted(aaData_rows, key=lambda x: x[sortInd], reverse=(sortAsc != 'asc'))
    else:
        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    for i,row in enumerate(aaData_rows):
        row[2] = ttPresenter.getHref(row[1], row[2])
        row[0] = (i + 1)

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows[leftInd:rightInd]
    results = output
    return json.dumps(results)


@ttstat.route("/_retrieve_players_data")
def get_players_data():
    print(request.values)
    print(request.values['sSortDir_0'])
    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
    output['sEcho'] = str(int(request.values['sEcho']))
    output['iTotalRecords'] = str(len(ttModel.players))
    c = 0

    text = request.values['sSearch'].lower()
    print(text)

    players = []
    for k,player in ttModel.players.items():
        if player.findString(text) is True:
            players.append(player)
        c += 1
    aaData_rows = ttPresenter.getPlayersTable(players)
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttPresenter.players_dtypes[sortInd] == 'string':
        aaData_rows = sorted(aaData_rows, key=lambda x: x[sortInd], reverse=(sortAsc != 'asc'))
    else:
        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows[leftInd:rightInd]

    results = output

    # return the results as a string for the datatable
    return json.dumps(results)


@ttstat.route("/_retrieve_competitions_data")
def get_competitions_data():
    columns = ttPresenter.competitions_columns

    sourceIdFilter = None
    if 'sourceId' in request.values:
         sourceIdFilter = request.values['sourceId']

    print(request.values)
    print(request.values['sSortDir_0'])
    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
    output['sEcho'] = str(int(request.values['sEcho']))
    output['iTotalRecords'] = str(len(ttModel.competitionsStorage.competitions))
    c = 0

    text = request.values['sSearch'].lower()
    print(text)

    competitions = []
    for comp in ttModel.competitionsStorage.competitions:
        if sourceIdFilter and not (sourceIdFilter in comp.sources):
            continue
        if comp.name.lower().find(text) != -1:
            competitions.append(comp)
        c += 1
    aaData_rows = ttPresenter.getCompetitionsTable(competitions)
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttPresenter.competitions_dtypes[sortInd] == 'string':
        aaData_rows = sorted(aaData_rows, key = lambda x: x[sortInd], reverse=(sortAsc!='asc'))
    else:
        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows[leftInd:rightInd]

    results = output

    # return the results as a string for the datatable
    return json.dumps(results)


def update(a, b):
    cur = db.cursor()
    cur.execute("SELECT * FROM fonbet_live WHERE datetime > '{}' ORDER BY datetime ASC".format(ttModel.lastUpdateTime))
    db.commit()
    ttModel.update(cur.fetchall())
