import datetime


class FeaturesFactory:
    def __init__(self):
        pass

    @staticmethod
    def getRankingsFeatures(rankingsStorage, id1, id2, dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        res = dict()
        for source in list(rankingsStorage.rankings) + list(rankingsStorage.dayRankings):
            ws = 5000
            if source == 'ittf':
                ws = 1000
            if source.endswith('_day'):
                r1 = rankingsStorage.getDayRanking(id1, source, dt[:10], dt[11:], ws=ws)
                r2 = rankingsStorage.getDayRanking(id2, source, dt[:10], dt[11:], ws=ws)
            else:
                r1 = rankingsStorage.getRanking(id1, source, dt[:10], ws=ws)
                r2 = rankingsStorage.getRanking(id2, source, dt[:10], ws=ws)
            res[source] = {'1': r1, '2': r2}
            res[source]['v'] = r1 - r2 if (r1 != -1 and r2 != -1) else 0
        return res

    @staticmethod
    def getOneVSOneFeatures(matchesStorage, id1, id2, dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        ovoMatches = matchesStorage.getOneVSOneMatches(id1, id2, dt[:10], dt[11:], ws=365)
        wins = [0, 0]
        sets = [0, 0]
        for ovoMatch in ovoMatches:
            for j in range(2):
                if ovoMatch.wins is not None:
                    wins[j] += ovoMatch.wins[j]
                if ovoMatch.sets is not None:
                    sets[j] += ovoMatch.sets[j]

        res = dict()
        res['ovo_win'] = {'1': wins[0], '2': wins[1]}
        res['ovo_win']['v'] = (wins[0] + 1e-9) / (wins[0] + wins[1] + 2e-9) - 0.5

        res['ovo_set'] = {'1': sets[0], '2': sets[1]}
        res['ovo_set']['v'] = (sets[0] + 1) / (sets[0] + sets[1] + 2) - 0.5

        return res