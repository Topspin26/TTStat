import numpy as np
import scipy as sp
import scipy.sparse as sps
from sklearn import linear_model


class RankingModel:
    def __init__(self):
        self.ids = []
        self.y = []
        self.w = []
        self.n = 0
        self.rn = 0
        self.fl = np.ones(1000000)
        self.rows = np.zeros(1000000)
        self.cols = np.zeros(1000000)
        self.vals = np.zeros(1000000)
        self.indexes = dict()

    def addMatches(self, ids, y, w):
        for id, y, w in zip(ids, y, w):
            self.y.append(y)
            self.w.append(w)
            arr = []
            for i in id[0]:
                arr.append(self.rn)
                self.rows[self.rn] = self.n
                self.cols[self.rn] = i
                self.vals[self.rn] = 1
                self.rn += 1

            for i in id[1]:
                arr.append(self.rn)
                self.rows[self.rn] = self.n
                self.cols[self.rn] = i
                self.vals[self.rn] = -1
                self.rn += 1
            self.indexes[self.n] = arr
            self.n += 1

    def removeMatches(self, ind):
        arr = []
        for i in ind:
            arr += self.indexes[i]
        self.fl[arr] = 0


class BradleyTerryRM(RankingModel):
    def __init__(self, model=None):
        self.model = model
        if self.model is None:
            self.model = linear_model.LogisticRegression(C=100, solver='newton-cg', fit_intercept=0)  # , warm_start=1)
        super().__init__()

    def calcRankings(self, model=None, matchesCntBorder=1):
        # mCnt = self.n
        y = np.array(self.y)
        w = np.array(self.w)
        x = sps.csr_matrix((self.vals[:self.rn][self.fl[:self.rn] != 0],
                            (self.rows[:self.rn][self.fl[:self.rn] != 0],
                             self.cols[:self.rn][self.fl[:self.rn] != 0])))
        cm = np.absolute(x).sum(axis=0)

        indNonZero = np.nonzero(cm[0] >= matchesCntBorder)[1].tolist()
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

#        if self.model.coef_ is not None:
#            print(len(self.model.coef_[0]))
        self.model.fit(xx, yy, sample_weight=ww * 10)
        r = np.append(self.model.coef_, -self.model.coef_.sum())

        res = []
        for i in range(cm.shape[1]):
            rr = float('nan')
            if i in indNonZero:
                ind = indNonZero.index(i)
                rr = r[ind]
            res.append(rr)
        return res