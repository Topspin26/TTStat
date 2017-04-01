from os import walk
import time
import datetime as datetime
import random
import re

from Entity import *
from Storages import *
from common import *
import statsmodels.api as sm
import numpy as np
import scipy as sp
import scipy.sparse as sps
from sklearn import linear_model
import math

def getPoints(pointsScore):
    res = [0, 0]
    for e in pointsScore.split(';'):
        try:
            tt = e.split(':')
            res[0] += int(tt[0])
            res[1] += int(tt[1])
        except:
            pass
    return res

def getPlayerId(player, men2_players, women2_players):
    res = '0'
    if player in men2_players:
        res = men2_players[player][0]
    if player in women2_players:
        res = women2_players[player][0]
    return res

def calcLH(x, y, w, r):
    res = 0
    for i in range(len(y)):
        f = 0
        for j in range(3):
            f += x[i, j] * r[j] 
        if y[i] == 1:
            res += w[i] * math.log(1.0 / (1.0 + math.exp(-f)))
        else:
            res += w[i] * math.log(1.0 / (1.0 + math.exp(f)))
    return -res / len(y)

def foo1():
    x1 = sps.lil_matrix((10, 3))
    y1 = np.ones(10)
    x1[0:4, 0] = 1; x1[0:4, 1] = -1
    y1[3] = 0
    x1[4:8, 1] = 1; x1[4:8, 2] = -1
    y1[6:8] = 0
    x1[8:10,:] = -1;
    y1[9] = 0
    model1 = sm.Logit(y1, x1.toarray())
    result1 = model1.fit()
    print(result1.params)
    print(result1.summary())
 
    x2 = sps.lil_matrix((8, 2))
    y2 = np.ones(8)
    x2[0:4, 0] = -1; x2[0:4, 1] = 1
    y2[0:3] = 0
    x2[4:8, 1] = 2; x2[4:8, 0] = 1
    y2[6:8] = 0
    model2 = sm.Logit(y2, x2.toarray())
    result2 = model2.fit()
    print(result2.params)
    print(result2.summary())

    x3 = sps.lil_matrix((8, 2))
    y3 = np.ones(8)
    x3[0:4, 0] = 2; x3[0:4, 1] = 1
    y3[3] = 0
    x3[4:8, 1] = -2; x3[4:8, 0] = -1
    y3[6:8] = 0
    model3 = sm.Logit(y3, x3.toarray())
    result3 = model3.fit()
    print(result3.params)
    print(result3.summary())
    
#    foo = np.array([[1, -1], [1, -1], [1, -1], [1, -1], [1, 1], [1, 1]])
#    print(np.dot(foo.T, foo))

    X1 = x1.toarray()
    p1 = result1.predict(X1)
#    print(p)
    V1 = np.diag(np.multiply(p1, 1 - p1))
    C1 = sp.linalg.inv(x1.T * V1 * x1)
    print()
#    print(V)
#    print(np.dot(X.T, V))
#    print(np.dot(np.dot(X.T, V), X))
    SE1 = np.sqrt(C1)
    print(SE1)

    X2 = x2.toarray()
    p2 = result2.predict(X2)
#    print(p)
    V2 = np.diag(np.multiply(p2, 1 - p2))
    C2 = sp.linalg.inv(x2.T * V2 * x2)
    print()
#    print(V)
#    print(np.dot(X.T, V))
#    print(np.dot(np.dot(X.T, V), X))
    SE2 = np.sqrt(C2)
    print(SE2)
    D = np.array([-1.0, -1.0])
    print(np.sqrt(np.dot(np.dot(D, C2), D.T)))
    
    X3 = x3.toarray()
    p3 = result3.predict(X2)
#    print(p)
    V3 = np.diag(np.multiply(p3, 1 - p3))
    C3 = sp.linalg.inv(x3.T * V3 * x3)
    print()
#    print(V)
#    print(np.dot(X.T, V))
#    print(np.dot(np.dot(X.T, V), X))
    SE3 = np.sqrt(C3)
    print(SE3)
    D = np.array([-1.0, -1.0])
    print(np.sqrt(np.dot(np.dot(D, C3), D.T)))
    
    return
    
    z = sp.stats.norm.ppf(0.975) #(dof).ppf(0.975)
    print((result.params[0] - z * SE[0, 0], result.params[0] + z * SE[0, 0]))
    return

    V1 = np.diag([0.75 * 0.25 * 4, 0.5 * 0.5 * 2])
    X1 = np.array([[1.0, -1.0], [-1.0, -1.0]])  
    print(np.dot(np.dot(X1.T, V1), X1))
    C1 = np.linalg.inv(np.dot(np.dot(X1.T, V1), X1))
    SE1 = np.sqrt(C1)
    print(SE1)


def foo():
    x = sps.lil_matrix((4, 3))
    y = np.ones(4)
    w = np.ones(4)
    w[3] = 0.5
    x[0, 0] = 1; x[0, 1] = -1; w[0] = 0.75
    x[1, 1] = 1; x[1, 2] = -1; w[1] = 1
    x[2, 2] = 1; x[2, 0] = -1; w[2] = 1
    x[3, :] = 1
    xx = sps.lil_matrix(sps.vstack([x, x]))
    yy = np.hstack([y, 1 - y])
    ww = np.hstack([w, 1 - w])
#    print(np.hstack([xx.toarray(), np.transpose(np.vstack([yy, ww]))]))
    
    model = linear_model.LogisticRegression(C = 1e10, solver = 'newton-cg', fit_intercept = False)
    model.fit(xx, yy, sample_weight = ww)
    print(model.coef_)
    print(type(xx))
    print(calcLH(xx, yy, ww, model.coef_[0]))
    
    x1 = sps.lil_matrix((38, 3))
    y1 = np.ones(38)
    y1[9:12] = 0
    x1[0:12, 0] = 1; x1[0:12, 1] = -1;
    x1[12:24, 1] = 1; x1[12:24, 2] = -1;
    x1[24:36, 2] = 1; x1[24:36, 0] = -1;
    x1[36:38,:] = 1;
    y1[37] = 0
#    print(np.hstack([x1.toarray(), np.transpose(np.asmatrix(y1))]))
    model = linear_model.LogisticRegression(C = 1e10, solver = 'newton-cg', fit_intercept = False)
    model.fit(x1, y1)
    print(model.coef_)
#    print(calcLH(xx, yy, ww, model.coef_[0]))

    model0 = sm.Logit(y1, x1.toarray())
    result = model0.fit()
    print(result.params)
#    print(calcLH(xx, yy, ww, result.params))
    print(result.summary())

    X = x1.tocsr() 
#    X = x1.toarray()
    p = result.predict(x1.toarray())
    V = np.diag(np.multiply(p, 1 - p))
    C = sp.linalg.inv(X.T * V * X)
    SE = np.sqrt(C)
    print(SE)
    
    V1 = np.diag([V[0, 0] * 1, V[12, 12] * 1, V[24, 24] * 1, V[36, 36] * 1])
    X1 = x.toarray()  
    C1 = np.linalg.inv(np.dot(np.dot(X1.T, V1), X1))
    SE1 = np.sqrt(C1)
    print(SE1)
    return

    i = 2
    beta, c = result.params[i], SE[i,i]
     
    N = result.nobs
    P = result.df_model
    dof = N - P - 1
    z = sp.stats.norm.ppf(0.975) #(dof).ppf(0.975)
    print((beta - z * c, beta + z * c))
    
    return

    # add a column of ones for the constant intercept term
     
    # convert the NumPy arrray to matrix
     
    # perform the matrix multiplication,
    # and then take the inverse
     
    for e in dir(result):
        try:
            print(getattr(result, e))
        except:
            pass
    # multiply by the MSE of the residual
    model1 = sm.OLS(y1, x1.toarray())
    result1 = model1.fit()
    print(result1.mse_resid)
    print(dir(result1))

    C *= 4
     
    # take the square root
    SE = np.sqrt(C)

    i = 0
    
    # the estimated coefficient, and its variance
    beta, c = result.params[i], SE[i,i]
     
    # critical value of the t-statistic
    N = result.nobs
    P = result.df_model
    dof = N - P - 1
    z = sp.stats.t( dof ).ppf(0.975)
     
    # the confidence interval
    print((beta - z * c, beta + z * c))


from sklearn import linear_model


class RankingModel:
    def __init__(self):
        self.matches = []
        self.n = 0

    def addMatch(self, match):
        self.matches.append(match)

class BradleyTerryRM(RankingModel):
    @staticmethod
    def calcRankings(ids, y, w, model=None):
        rows = []
        cols = []
        vals = []
        k = 0
        for id in ids:
            for i in id[0]:
                rows.append(k)
                cols.append(i)
                vals.append(1)

            for i in id[1]:
                rows.append(k)
                cols.append(i)
                vals.append(-1)

            k += 1

        mCnt = k
        y = np.array(y)
        w = np.array(w)
        x = sps.csr_matrix((vals, (rows, cols)))
        cm = np.absolute(x).sum(axis=0)

        indNonZero = np.nonzero(cm[0] > 0)[1].tolist()
        x = x[:, indNonZero]
        xv = x[:, -1].toarray().flatten()
        x = sps.lil_matrix(x)
        print(x.shape)
        for i in np.nonzero(xv)[0]:
            xi = x[i, -1]
            x[i] = x[i].toarray() - xi
        x = sps.lil_matrix(sps.csr_matrix(x)[:, :-1])
        print(x.shape)

        xx = sps.vstack([x, x])
        yy = np.hstack([y, 1 - y])
        ww = np.hstack([w, 1 - w])

        if model is None:
            model = linear_model.LogisticRegression(C=100, solver='newton-cg', fit_intercept=False)
        model.fit(xx, yy, sample_weight=ww * 10)
        r = np.append(model.coef_, -model.coef_.sum())

        res = []
        for i in range(cm.shape[1]):
            rr = float('nan')
            if i in indNonZero:
                ind = indNonZero.index(i)
                rr = r[ind]
            res.append(rr)
        return res


def calcRankings(matches, curDate, playersDict, mw, daysCnt = 365, matchesCntBorder = 16):
    mCnt = len(matches)
    #x = sps.lil_matrix((mCnt, len(playersDict.id2names)))
    y = np.ones(mCnt)
    w = np.ones(mCnt)
    ids = []

#    matchesList = []
    k = 0
    playerMatchesCnt = dict()
    for match in matches:
        mDate = match.date
        if mDate < curDate:
            fl_mw = ''
            for e in match.players[0] + match.players[1]:
                fl_mw += e[0]
            fl_mw = ''.join(sorted(set(list(fl_mw))))

            if match.isPair == 0 and fl_mw == mw:
                id = [match.players[0][0], match.players[1][0]]
    #            if not (match.points is None) and not (match.sets is None):
                if not (match.sets is None):
                    if (mDate > (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() - datetime.timedelta(days=daysCnt)).strftime("%Y-%m-%d")) or \
                            playerMatchesCnt.get(id[0], 0) < matchesCntBorder or playerMatchesCnt.get(id[1], 0) < matchesCntBorder:
                        playerMatchesCnt[id[0]] = playerMatchesCnt.get(id[0], 0) + 1
                        playerMatchesCnt[id[1]] = playerMatchesCnt.get(id[1], 0) + 1
                        ind = [(int(e[1:]) - 1) for e in id]
                        #x[k, ind] = [1, -1]
                        #points = match.getSumPoints()
                        #w[k] = (points[0] + 1) * 1.0 / (sum(points) + 2)
                        w[k] = (match.sets[0] + 0.2) * 1.0 / (match.sets[0] + match.sets[1] + 0.4)
                        #w[k] = (match.wins[0] + 1) * 1.0 / (match.wins[0] + match.wins[1] + 2)
                        k += 1
                        ids.append([[ind[0]], [ind[1]]])
    #                    matchesList.append(match)

    mCnt = k
    print(mCnt)
    r = BradleyTerryRM.calcRankings(ids, y[:mCnt], w[:mCnt])

    '''
    cm = np.absolute(x).sum(axis=0)
    indNonZero = np.nonzero(cm[0] > 3)[1].tolist()
#    print(indNonZero)

    x_new = sps.lil_matrix(sps.csr_matrix(x)[:, indNonZero])
    print(x_new.get_shape())
    #    print(np.nonzero(cm[0] > 0)[1].tolist())
    x_new = x_new.reshape((mCnt + 1, x_new.get_shape()[1]))
    x_new1 = sps.lil_matrix(x_new)
    x_new = x_new.tocsr()
    for i in range(x_new.shape[0]):
        if x_new[i, -1] != 0:
            for j in range(x_new.shape[1]):
                x_new1[i, j] -= x_new[i, -1]

    xnew_2 = sps.lil_matrix(sps.csr_matrix(x_new1)[:-1, :-1])
    ynew_2 = np.resize(y, mCnt)
    wnew_2 = np.resize(w, mCnt)

#    print(xnew_2.shape)
#    print(ynew_2.shape)
#    print(wnew_2.shape)

    xx2 = sps.lil_matrix(sps.vstack([xnew_2, xnew_2]))
    yy2 = np.hstack([ynew_2, 1 - ynew_2])
    ww2 = np.hstack([wnew_2, 1 - wnew_2])

    model = linear_model.LogisticRegression(C=1e10, solver='newton-cg', fit_intercept=False)
    model.fit(xx2, yy2, sample_weight=ww2 * 10)

    r = np.append(model.coef_[0], -model.coef_.sum())
    '''

    res = []
    for e in sorted(playersDict.id2names):
        if e[0] != mw:
            continue
        id = int(e[1:]) - 1
        if id < len(r) and r[id] == r[id]:
            res.append([e, playersDict.getName(e), r[id]])
    return res

def calcRankingsProcess(mw):
    playersDict = GlobalPlayersDict()

    sources = []
    sources.append(['master_tour', 'prepared_data/master_tour/all_results.txt'])
    sources.append(['liga_pro', 'prepared_data/liga_pro/all_results.txt'])
#    sources.append(['challenger_series', 'prepared_data/challenger_series/all_results.txt'])
    sources.append(['bkfon', 'prepared_data/bkfon/all_results.txt'])
    sources.append(['local', 'prepared_data/local/kchr_results.txt'])
    sources.append(['ittf', 'prepared_data/ittf/all_results.txt'])
    sources.append(['rttf', 'prepared_data/rttf/all_results.txt'])

    matchesStorage = MatchesStorage(sources)

    print(len(matchesStorage.matches))

    rankings = []
    startDate = '2015-12-28'
#    startDate = '2017-01-02'
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    curDate = startDate
    while curDate <= today:
        curDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        print(curDate)
        res = calcRankings(matchesStorage.matches, curDate, playersDict, mw, 730)
        for i, e in enumerate(sorted(res, key=lambda x: x[2], reverse=True)):
            rankings.append([curDate, e[0], str(e[2]), str(i + 1)])

    '''
    rankings = []
    year = 2017
    month = 4
    curDate = str(year) + '-' + str(month).zfill(2) + '-01'
    res = calcRankings(matchesStorage.matches, curDate, playersDict, mw, 730)
    for i, e in enumerate(sorted(res, key=lambda x: x[2], reverse=True)):
        rankings.append([curDate[:-3], e[0], str(e[2]), str(i + 1)])
    '''

    with open('test/all_rankings_' + mw + '.txt', 'w', encoding='utf-8') as fout:
        for e in rankings:
            fout.write('\t'.join(e) + '\n')
    return rankings


def main():
#    foo1()
#    return

    rankingsM = calcRankingsProcess('m')
    rankingsW = calcRankingsProcess('w')

    with open('test/all_rankings_mw_fresh.txt', 'w', encoding='utf-8') as fout:
        for e in rankingsM + rankingsW:
            fout.write('\t'.join(e) + '\n')

    return

#    matches = matches[:10000]
#    for e in men2_players.items():
#        print(e)
#    for e in women2_players.items():
#        print(e)

    mCnt = len(matches)
    x = sps.lil_matrix((mCnt, len(men_players) + len(women_players)))
    y = np.ones(mCnt)
    w = np.ones(mCnt)
    
#    w[3] = 0.5
#    x[3, :] = 1
#    xx = sps.lil_matrix(sps.vstack([x, x]))
#    yy = np.hstack([y, 1 - y])
#    ww = np.hstack([w, 1 - w])

    k = 0
    k1 = 0
    for match in matches:
        mDate = match.date
        mTime = match.time
        id = [match.players[0][0], match.players[1][0]]
        if not (match.points is None) and not (match.sets is None):
            points = match.getSumPoints()
    #            points = [int(e) + 1 for e in tokens[5:7]]
    #        setsScore = tokens[11]
    #        pointsScore = tokens[12]
            ind = [(int(e[1:]) - 1) for e in id]
#            print(ind)
            x[k, ind] = [1, -1]
            #w[k] = (points[0] + 1) * 1.0 / (sum(points) + 2)
            #w[k] = (match.sets[0] + 1) * 1.0 / (match.sets[0] + match.sets[1] + 2)
            w[k] = (match.wins[0] + 1) * 1.0 / (match.wins[0] + match.wins[1] + 2)
            k += 1
    mCnt = k
    print(mCnt)

    cm = np.absolute(x).sum(axis=0)
    indNonZero = np.nonzero(cm[0] > 2)[1].tolist()
    print(indNonZero)

    x_new = sps.lil_matrix(sps.csr_matrix(x)[:,indNonZero])
    print(x_new.get_shape())
#    print(np.nonzero(cm[0] > 0)[1].tolist())
#    xnew_2 = x_new.reshape((mCnt, x_new.get_shape()[1]))
    x_new = x_new.reshape((mCnt + 1, x_new.get_shape()[1]))
    x_new1 = sps.lil_matrix(x_new) 
    x_new = x_new.tocsr()
#    print(x_new.toarray())
    for i in range(x_new.shape[0]):
        if x_new[i, -1] != 0:
            for j in range(x_new.shape[1]):
                x_new1[i, j] -= x_new[i, -1]
#    print(x_new.tocsr()[10, 20])
#    print(x_new1.toarray())
    
    xnew_2 = sps.lil_matrix(sps.csr_matrix(x_new1)[:-1,:-1])
    
#    print(xnew_2.toarray())
    ynew_2 = np.resize(y, mCnt)
    wnew_2 = np.resize(w, mCnt)
    y = np.resize(y, mCnt + 1)
    w = np.resize(w, mCnt + 1)
    x_new[mCnt, :] = 1
    w[mCnt] = 0.5

    print(x_new.shape)
    print(y.shape)
    print(w.shape)

    print(xnew_2.shape)
    print(ynew_2.shape)
    print(wnew_2.shape)

    xx = sps.lil_matrix(sps.vstack([x_new, x_new]))
    yy = np.hstack([y, 1 - y])
    ww = np.hstack([w, 1 - w])

#    print(xnew_2.toarray())
    xx2 = sps.lil_matrix(sps.vstack([xnew_2, xnew_2]))
    yy2 = np.hstack([ynew_2, 1 - ynew_2])
    ww2 = np.hstack([wnew_2, 1 - wnew_2])


    model = linear_model.LogisticRegression(C = 1e10, solver = 'newton-cg', fit_intercept = False)
    model.fit(xx, yy, sample_weight = ww * 10)
#    print(model.coef_)

    model = linear_model.LogisticRegression(C = 1e10, solver = 'newton-cg', fit_intercept = False)
    model.fit(xx2, yy2, sample_weight = ww2 * 10)

    r = np.append(model.coef_[0], -model.coef_.sum())
    print(r)

    '''
    X = xx2.tocsr()
#    X = x1.toarray()
    p = model.predict_proba(xx2)[:, 1]
    V = sps.diags(np.multiply(p, 1 - p) * 10)
    print(V)
    C = sps.linalg.inv(X.T * V * X)
    print(C.toarray())
    SE = np.sqrt(C)

    D = np.array([-1.0] * (len(r) - 1))

    SEn = np.sqrt(np.dot(np.dot(D, C), D.T))
    print(SEn.shape)
    print(SE.shape)
    SE = np.append(SE.diagonal(), SEn)

    print(SE)

    z = sp.stats.norm.ppf(0.975)
#    r0 = r - z * SE
#    r1 = r + z * SE
    '''

#    print(model.coef_[0])
#    print(model.coef_[0] - z * np.diag(SE))
#    print(model.coef_[0] + z * np.diag(SE))
    
    res = []
    for e in sorted(men_players.keys()):
        id = int(e[1:]) - 1
        rr = rr0 = rr1 = -100
        if id in indNonZero:
            ind = indNonZero.index(id)
            rr = r[ind]
            #rr0 = r0[ind]
            #rr1 = r1[ind]
        res.append([e, men_players[e], cm[0, id], rr])#, rr0, rr1])
    with open('test/rankings_wins.txt', 'w', encoding = 'utf-8') as fout:
        for e in sorted(res, key = lambda x: x[3], reverse = True):
            fout.write(str(e) + '\n')

if __name__ == "__main__":
    main()