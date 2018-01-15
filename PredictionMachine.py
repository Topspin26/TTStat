# import pandas as pd
# import xgboost as xgb
# import pickle

import datetime
import numpy as np
from sklearn import linear_model
from TTMatchModel import TTMatchModel
from Entity import MatchBet
from FeaturesFactory import FeaturesFactory

class PredictionMachine:
    def __init__(self):

        self.model = linear_model.LogisticRegression(fit_intercept=False)
        self.features = ['ranking_my_730_4', 'ranking_my_730_4_day', 'ovo_win', 'ovo_set', 'bkfon']
        self.model.coef_ = np.array([[ 0.27756657,
                                       0.45927953,
                                       -0.16165021,
                                       0.75751843,
                                       0.59457467]])
        self.model.intercept_ = 0

        self.rankingsStorage = None
        self.matchesStorage = None

    def setRankingsStorage(self, rankingsStorage):
        self.rankingsStorage = rankingsStorage

    def setMatchesStorage(self, matchesStorage):
        self.matchesStorage = matchesStorage

    def getFeatures(self, match, dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score=None, betInfo=None):
        allFeatures = dict()
        mw = match.getMW()
        if mw not in {'mm', 'ww'}:
            return allFeatures

        id1 = match.ids[0][0]
        id2 = match.ids[1][0]

        rankingsFeatures = FeaturesFactory.getRankingsFeatures(self.rankingsStorage, id1, id2, dt)
        ovoFeatures = FeaturesFactory.getOneVSOneFeatures(self.matchesStorage, id1, id2, dt)

        allFeatures.update(rankingsFeatures)
        allFeatures.update(ovoFeatures)

        k1, k2 = betInfo.get('win1', [1, -1])[0], betInfo.get('win2', [1, -1])[0]
        allFeatures['bkfon'] = {'1': k1, '2': k2}
        allFeatures['bkfon']['v'] = np.log(max(k2, 1.0) / max(k1, 1.0))

        return allFeatures

    def predict(self, match, dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score=None, betInfo=None):
        mw = match.getMW()
        if mw not in {'mm', 'ww'}:
            return -1

        allFeatures = self.getFeatures(match, dt=dt, score=score, betInfo=betInfo)

        # id1 = match.ids[0][0]
        # id2 = match.ids[1][0]

        x = np.array([allFeatures.get(e, {'v': 0}).get('v', 0) for e in self.features]).reshape(1, -1)
        pWin = self.model.predict_proba(x)[:, 1]
        if score is not None:
            sets, points, setsCnt = MatchBet.parseScore(score, isParsed=True)
            if setsCnt is not None and setsCnt > max(sets):
                if points[0][0] + points[1][0] == 0:
                    print(x)
                    print(score, sets, points, setsCnt)
                return TTMatchModel.predictPWinByScore(pWin, setsCnt, sets, [points[0][-1], points[1][-1]])
            else:
                return -1
        return pWin, allFeatures