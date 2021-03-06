from Entity import Match
from common import *
from Storages import *
from RankingModel import BradleyTerryRM


def calcSetWeight(match):
    return (match.sets[0] + 0.1) * 1.0 / (match.sets[0] + match.sets[1] + 0.2)
def calcWinWeight(match):
    return 0.95 * match.wins[0] + 0.05 * match.wins[1]


def run(playersDict, matchesStorage, mw, params, rightDate):
    matches = matchesStorage.matches

    events = []
    k = 0
    for match in sorted(matches, key=lambda x: x.date):
        if match.isPair == 0 and mw+mw == match.getMW():
            if match.sets is not None:
                events.append([match.date, 1, k, match])
                removeDate = (datetime.datetime.strptime(match.date, "%Y-%m-%d").date() +
                              datetime.timedelta(days=params['ws'])).strftime("%Y-%m-%d")
                events.append([removeDate, 0, k, match])
                k += 1

    rm = BradleyTerryRM()

    rankings = dict()
    rankings[params['name']] = []

    curDate = None
    for dt, fl, k, match in sorted(events, key=lambda x: x[0] + '_' + str(x[1])):
        if curDate != dt:
            if curDate is not None and '2017-12-25' <= curDate <= rightDate:
            # if curDate is not None and '2015-12-31' <= curDate <= rightDate:
                outDate = (datetime.datetime.strptime(curDate, '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                print(outDate)
                r, matchesCnt = rm.calcRankings(matchesCntBorder=params['matchesCntBorder'])

                res = []
                for e in sorted(playersDict.id2names):
                    if e[0] != mw:
                        continue
                    id = int(e[1:]) - 1
                    if id < len(r) and r[id] == r[id]:
                        res.append([e, playersDict.getName(e), r[id], matchesCnt[id]])

                for i, e in enumerate(sorted(res, key=lambda x: x[2], reverse=True)):
                    rankings[params['name']].append([outDate, e[0], str(e[2]), str(i + 1), str(e[3])])

            curDate = dt
        if fl == 1:
            ind = [(int(e[1:]) - 1) for e in [match.ids[0][0], match.ids[1][0]]]
            w = params['wf'](match)
            rm.addMatches([[[ind[0]], [ind[1]]]], [1], [w])
        elif fl == 0:
            rm.removeMatches([k])
        else:
            break

    for k, v in rankings.items():
        with open('prepared_data/rankings/rankings_' + mw + '_' + k + '.txt', 'a', encoding='utf-8') as fout:
            for e in v:
                fout.write('\t'.join(e) + '\n')



def main():
    playersDict = GlobalPlayersDict("filtered")

    sources = []
    sources.append(['master_tour', 'prepared_data/master_tour/all_results.txt'])
    sources.append(['liga_pro', 'prepared_data/liga_pro/all_results.txt'])
    sources.append(['challenger_series', 'prepared_data/challenger_series/all_results.txt'])
    #sources.append(['bkfon', 'prepared_data/bkfon/all_results.txt'])
    sources.append(['local', 'prepared_data/local/kchr_results.txt'])
    sources.append(['ittf', 'prepared_data/ittf/all_results.txt'])
    sources.append(['rttf', 'prepared_data/rttf/all_results.txt'])

    matchesStorage = MatchesStorage(sources)


    sourcesSet0 = {e[0] for e in sources}
    sourcesSet1 = {'master_tour', 'liga_pro', 'challenger_series', 'local', 'ittf'}

    #mw = 'm'
    rightDate = (datetime.datetime.now()).strftime('%Y-%m-%d')
    for ws in [730]:
        for matchesCntBorder in [1, 4]:
            params = dict()
            params['ws'] = ws
            params['matchesCntBorder'] = matchesCntBorder
            params['wf'] = calcSetWeight
            params['sources'] = sourcesSet0
            params['name'] = 'sets_sources=0_ws=' + str(ws) + '_matchesCntBorder=' + str(matchesCntBorder)
            for mw in ['m', 'w']:
                run(playersDict, matchesStorage, mw, params, rightDate)


if __name__ == "__main__":
    main()