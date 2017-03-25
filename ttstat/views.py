
from flask import render_template, request, flash, redirect
from ttstat import ttstat, ttModel
import simplejson as json
from .models import TTModel

@ttstat.route('/')
@ttstat.route('/index')
def index():
    return render_template('index.html')

@ttstat.route('/matches')
def matches():
    return render_template('matches.html', matches_columns = ttModel.matches_columns, bets_columns = ttModel.bets_columns)

@ttstat.route('/players')
def players():
    return render_template('players.html', columns = ttModel.players_columns)

@ttstat.route('/players/<id>')
def player_info(id):
    return render_template('player_info.html', id = id, name = ttModel.getPlayerNames(id),
                           matches_columns = ttModel.matches_columns,
                           rankings_columns = ttModel.player_rankings_columns,
                           bets_columns=ttModel.bets_columns)

@ttstat.route('/rankings')
def rankings():
    return render_template('rankings.html', columns = ttModel.rankings_columns, sex = 'men')

@ttstat.route('/rankings/<sex>')
def rankings1(sex):
    return render_template('rankings.html', columns = ttModel.rankings_columns, sex = sex)

@ttstat.route('/prognosis')
def prognosis():
    return render_template('prognosis.html', columns = ttModel.players_columns)

@ttstat.route('/selectPlayer', methods = ['POST'])
def selectPlayer():
    playerId = request.values['playerId']
    print(playerId)
    res = dict()
    res['status'] = 'OK'
    res['playerId'] = playerId
    res['playerName'] = ttModel.getPlayerName(playerId)
    res['playerR'] = str(ttModel.getFeatures(playerId, '2017-01-30'))
    return json.dumps(res)

@ttstat.route('/makePrognosis', methods = ['POST'])
def makePrognosis():
    playerId1 = request.values['playerId1']
    playerId2 = request.values['playerId2']
    print([playerId1, playerId2])
    res = dict()
    res['status'] = 'OK'

    res['pred'] = ttModel.makePrediction(playerId1, playerId2)
    print(res['pred'])
    return json.dumps(res)


@ttstat.route("/_retrieve_matches_data")
def get_matches_data():
    columns = ttModel.matches_columns

    playerIdFilter = None
    if 'playerId' in request.values:
        playerIdFilter = request.values['playerId']
    print(playerIdFilter)

    print(request.values)
    print(request.values['sSortDir_0'])
    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
    output['sEcho'] = str(int(request.values['sEcho']))

    sources = None
    if 'sources' in request.values:
        sources = set(request.values['sources'].strip(';').split(';'))
    print(sources)

    text = request.values['sSearch'].lower()
    print(text)
    aaData_rows = []
    c = 0
    #ys = td.y.sum(axis=1)

    matches = []
    matchesList = ttModel.matches
    if not (playerIdFilter is None):
        matchesList = ttModel.players[playerIdFilter].matches
    output['iTotalRecords'] = str(len(matchesList))
    for match in matchesList:
        flMatch = 0
        for src in match.sources:
            if (sources is None) or (src in sources):
                flMatch = 1
        if flMatch == 0:
            continue
        flMatch = 0
        for i in range(2):
            for player in match.players[i]:
                if ttModel.players[player].findString(text) == True:
                    flMatch = 1
#        if (' - '.join(ttModel.getNames(match.players[0]))).lower().find(text) != -1 or (' - '.join(ttModel.getNames(match.players[1]))).lower().find(text) != -1:
        if flMatch == 1:
            matches.append(match)
            c += 1
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    print([sortInd, ttModel.matches_dtypes[sortInd]])
    aaData_rows = ttModel.getMatchesTable(matches, sortInd, int(sortAsc == 'asc'))

#    if ttModel.matches_dtypes[sortInd] == 'string':
#        aaData_rows = sorted(aaData_rows, key = lambda x: x[sortInd], reverse=(sortAsc!='asc'))
#    else:
#        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows[leftInd:rightInd]

    results = output
    return json.dumps(results)

@ttstat.route("/_retrieve_match_bets_data")
def get_match_bets_data():
    columns = ttModel.bets_columns

    print(request.values)
    print(request.values['sSortDir_0'])
    #leftInd = int(request.values['iDisplayStart'])
    #rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
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
    columns = ttModel.player_rankings_columns

    playerIdFilter = None
    if 'playerId' in request.values:
        playerIdFilter = request.values['playerId']
    print(playerIdFilter)

    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
    output['sEcho'] = str(int(request.values['sEcho']))

    c = 0
    output['iTotalRecords'] = 0
    aaData_rows = []
    if playerIdFilter in ttModel.rusRankings:
        output['iTotalRecords'] += len(ttModel.rusRankings[playerIdFilter])
        for e in sorted(ttModel.rusRankings[playerIdFilter].items(), key = lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'TTFR', e[1][0], e[1][1]])
            c += 1
    if playerIdFilter in ttModel.ittfRankings:
        output['iTotalRecords'] += len(ttModel.ittfRankings[playerIdFilter])
        for e in sorted(ttModel.ittfRankings[playerIdFilter].items(), key = lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'ITTF', e[1][0], e[1][1]])
            c += 1
    if playerIdFilter in ttModel.myRankings:
        output['iTotalRecords'] += len(ttModel.myRankings[playerIdFilter])
        for e in sorted(ttModel.myRankings[playerIdFilter].items(), key = lambda x: x[0], reverse=True):
            aaData_rows.append([e[0], 'MY', e[1][0], e[1][1]])
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
    columns = ttModel.rankings_columns

#    playerIdFilter = None
#    if 'playerId' in request.values:
#        playerIdFilter = request.values['playerId']
#    print(playerIdFilter)

    leftInd = int(request.values['iDisplayStart'])
    rightInd = leftInd + int(request.values['iDisplayLength'])
    output = {}
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
            if player.findString(text) == True:
                r = ttModel.getRankings(player.id, dt, 100)
                aaData_rows.append(['0', player.id, player.name, r['rus'], r['ittf'], r['my']])
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
    columns = ttModel.players_columns

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
        if player.findString(text) == True:
            players.append(player)
        c += 1
    aaData_rows = ttModel.getPlayersTable(players)
    sortInd = int(request.values['iSortCol_0'])
    sortAsc = request.values['sSortDir_0']
    if ttModel.players_dtypes[sortInd] == 'string':
        aaData_rows = sorted(aaData_rows, key = lambda x: x[sortInd], reverse=(sortAsc!='asc'))
    else:
        aaData_rows = sorted(aaData_rows, key=lambda x: float(x[sortInd]), reverse=(sortAsc != 'asc'))

    output['iTotalDisplayRecords'] = str(c)

    output['aaData'] = aaData_rows[leftInd:rightInd]

    results = output

    # return the results as a string for the datatable
    return json.dumps(results)


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
