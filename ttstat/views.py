from flask import render_template, request, flash, redirect
from ttstat import ttstat, ttModel, db
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
                           matches_columns=ttModel.matches_columns,
                           bets_columns=ttModel.bets_columns,
                           filters=filters)


@ttstat.route('/matches/<matchId>')
def match_info(matchId):
    filters = dict()
    match = ttModel.getMatch(matchId).toDict()
    match['players'] = [ttModel.getPlayersHrefsByIdsNames(e1, e2) for e1, e2 in zip(match['ids'], match['names'])]
    return render_template('match_info.html', bets_columns=ttModel.bets_columns, match=match, filters=filters)


@ttstat.route('/players')
def players():
    return render_template('players.html', columns=ttModel.players_columns)


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
                           matches_columns=ttModel.matches_columns,
                           rankings_columns=ttModel.player_rankings_columns,
                           bets_columns=ttModel.bets_columns, filters=filters)


@ttstat.route('/competitions')
def competitions():
    filters = dict()
    filters['sourceId'] = request.args.get('sourceId')
    filters['sourceName'] = request.args.get('sourceId')
#    if request.args.get('compId'):
#    filters['compId'] = request.args.get('compId')
#    filters['compName'] = ttModel.competitionsStorage.getCompName(request.args.get('compId'))
    return render_template('competitions.html', competitions_columns=ttModel.competitions_columns, filters=filters)


@ttstat.route('/competitions/<compId>')
def competition_info(compId):
    filters = dict()
    filters['compId'] = compId
    filters['compName'] = ttModel.competitionsStorage.getCompName(filters['compId'])
    return render_template('competitions.html', matches_columns=ttModel.matches_columns, bets_columns=ttModel.bets_columns, filters=filters)


@ttstat.route('/rankings')
def rankings():
    return render_template('rankings.html', columns=ttModel.rankings_columns, sex='men')


@ttstat.route('/sources')
def sources():
    return render_template('sources.html')


@ttstat.route('/sources/<sourceId>')
def source_info(sourceId):
    return render_template('sources.html')


@ttstat.route('/rankings/<sex>')
def rankings1(sex):
    return render_template('rankings.html', columns=ttModel.rankings_columns, sex=sex)


@ttstat.route('/prognosis')
def prognosis():
    return render_template('prognosis.html', columns=ttModel.players_columns)


@ttstat.route('/live')
def live():
    return render_template('live.html', columns=['datettime', 'eventId', 'compname', 'Игрок1', 'Игрок2', 'Счет', 'info'])


@ttstat.route('/live/<matchId>')
def live_match_info(matchId):
    filters = dict()
    match = ttModel.getLiveBet(matchId).toDict()
    match['players'] = [ttModel.getPlayersHrefsByIdsNames(e1, e2) for e1, e2 in zip(match['ids'], match['names'])]
    match['hash'] = match['key']
    return render_template('live_match_info.html', bets_columns=ttModel.bets_columns, match=match, filters=filters)


@ttstat.route("/_retrieve_live_data")
def retrieve_live_data():
#    cur = db.cursor()
#    cur.execute("SELECT * FROM fonbet_live WHERE datetime = (SELECT MAX(datetime) FROM fonbet_live)")
#    db.commit()
    aaData_rows = ttModel.getLiveBetsTable()
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
    aaData_rows = ttModel.getBetsTable()
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
                    if playerId != '':
                        for plId in playerId.split(','):
                            if ttModel.players[plId].findString(text) is True:
                                flMatch = 1
                    else:
                        if playerName.find(text) != -1:
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
    aaData_rows = ttModel.getMatchesTable(matches[leftInd:rightInd], filterFlag=True)

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
    aaData_rows = ttModel.getMatchBetsTable(matchHash, sortInd, int(sortAsc == 'asc'))

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
    if playerIdFilter in ttModel.rankingStorage.rankings['ttfr']:
        output['iTotalRecords'] += len(ttModel.rankingStorage.rankings['ttfr'][playerIdFilter])
        for e in sorted(ttModel.rankingStorage.rankings['ttfr'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'TTFR', e[1][0], e[1][1]])
            c += 1
    if playerIdFilter in ttModel.rankingStorage.rankings['ittf']:
        output['iTotalRecords'] += len(ttModel.rankingStorage.rankings['ittf'][playerIdFilter])
        for e in sorted(ttModel.rankingStorage.rankings['ittf'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'ITTF', e[1][0], e[1][1]])
            c += 1
    if playerIdFilter in ttModel.rankingStorage.rankings['my']:
        output['iTotalRecords'] += len(ttModel.rankingStorage.rankings['my'][playerIdFilter])
        for e in sorted(ttModel.rankingStorage.rankings['my'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'MY', format(float(e[1][0]),'.3f'), e[1][1]])
            c += 1
    if playerIdFilter in ttModel.rankingStorage.rankings['liga_pro']:
        output['iTotalRecords'] += len(ttModel.rankingStorage.rankings['liga_pro'][playerIdFilter])
        for e in sorted(ttModel.rankingStorage.rankings['liga_pro'][playerIdFilter].items(),
                        key=lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'LIGA-PRO', e[1][0], 0])
            c += 1
    output['iTotalRecords'] = str(output['iTotalRecords'])
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttModel.player_rankings_dtypes[sortInd] == 'string':
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
                aaData_rows.append(['0', player.id, player.name, r['rus'], r['ittf'], format(float(r['my']),'.3f'), r['liga_pro']])
                c += 1
            total += 1
    output['iTotalRecords'] = str(total)

    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttModel.rankings_dtypes[sortInd] == 'string':
        aaData_rows = sorted(aaData_rows, key=lambda x: x[sortInd], reverse=(sortAsc != 'asc'))
    else:
        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    for i,row in enumerate(aaData_rows):
        row[2] = ttModel.getHref(row[1], row[2])
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
    aaData_rows = ttModel.getPlayersTable(players)
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttModel.players_dtypes[sortInd] == 'string':
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
    columns = ttModel.competitions_columns

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
    aaData_rows = ttModel.getCompetitionsTable(competitions)
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttModel.competitions_dtypes[sortInd] == 'string':
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

'''
@myfirst.route('/player/<id>')
def player(id):
    player = Player.query.get(id)
    matches = player.matches1
    for i in range(len(matches)):
        matches[i].player2_name = Player.query.get(matches[i].player2_id).name

    return render_template('player.html',
                           title=None,
                           player=player,
                           matches=matches)


@myfirst.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)
'''

'''
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index1'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username



from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('myfirst.html', name=name)

from flask import request

def valid_login(user, login):
    return (login == user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    if valid_login(username, password):
        error = None
        #return log_the_user_in(request.form['username'])
    else:
        error = 'Invalid username/password'
#    if request.method == 'GET':
#        username = request.args.get('username', '')
#        password = request.args.get('password', '')
#        if ~valid_login(username, password):
#            error = None
#            #return log_the_user_in(request.form['username'])
#        else:
#            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
'''
