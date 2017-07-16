import numpy as np

class TTMatchModel:
    def __init__(self, pWin, setsCnt=5):
        self.pWin = pWin
        self.setsCnt = setsCnt
        self.pSet = TTMatchModel.calcPSet(self.pWin, self.setsCnt)
        self.pPointSet = TTMatchModel.calcPPoint(self.pSet)

    @staticmethod
    def calcPSet(pWin, setsCnt):
        l = 0
        r = 1
        while (r - l > 1e-8):
            x = (l + r) / 2
            if TTMatchModel.predictPWin(x, setsCnt) > pWin:
                r = x
            else:
                l = x
        return (l + r) / 2

    @staticmethod
    def calcPPoint(pSet):
        l = 0
        r = 1
        while (r - l > 1e-8):
            x = (l + r) / 2
            if TTMatchModel.predictPSet(x) > pSet:
                r = x
            else:
                l = x
        return (l + r) / 2

    @staticmethod
    def predictPWin(pSet, setsCnt, sets=[0, 0]):
        res = 0
        c = np.zeros((setsCnt + 1, setsCnt + 1))
        c[sets[0], sets[1]] = 1
        for i in range(setsCnt + 1):
            for j in range(setsCnt + 1):
                if i != 0 and j != setsCnt:
                    c[i, j] += c[i - 1, j] * pSet
                if i != setsCnt and j != 0:
                    c[i, j] += c[i, j - 1] * (1 - pSet)
                if i == setsCnt and j != setsCnt:
                    res += c[i, j]
        return res

    @staticmethod
    def predictPWinByScore(pWinStart, setsCnt, sets, points):
        pSet = TTMatchModel.calcPSet(pWinStart, setsCnt)
        pPoint = TTMatchModel.calcPPoint(pSet)
        pCur = TTMatchModel.predictPSet(pPoint, points=points)
        res = TTMatchModel.predictPWin(pSet, setsCnt, [sets[0] + 1, sets[1]]) * pCur
        res += TTMatchModel.predictPWin(pSet, setsCnt, [sets[0], sets[1] + 1]) * (1 - pCur)
        return res

    @staticmethod
    def predictPSet(pPoint, points=[0, 0]):
        b = min(points[0], points[1])
        if b > 10:
            points[0] -= (b - 10)
            points[1] -= (b - 10)
        if points[0] == 12 and points[1] == 10:
            return 1.
        if points[0] == 10 and points[1] == 12:
            return 0.
        res = 0
        pointsCnt = 11
        c = np.zeros((pointsCnt + 2, pointsCnt + 2))
        c[points[0], points[1]] = 1
        for i in range(pointsCnt + 1):
            for j in range(pointsCnt + 1):
                if (i != 0 and j != pointsCnt) or (i == pointsCnt and j == pointsCnt):
                    c[i, j] += c[i - 1, j] * pPoint
                if (i != pointsCnt and j != 0) or (i == pointsCnt and j == pointsCnt):
                    c[i, j] += c[i, j - 1] * (1 - pPoint)
                if i == pointsCnt and j <= pointsCnt - 2:
                    res += c[i, j]
#                print(i, j, c[i, j])
#                if i == pointsCnt - 1 and j == pointsCnt - 1:
#                    print(c[i, j])
        res += c[pointsCnt, pointsCnt - 1] * pPoint
#        print(9, 9, c[9, 9])
#        print(9, 10, c[9, 10])
#        print(10, 9, c[10, 9])
#        print(11, 9, c[11, 9])
#        print(9, 11, c[9, 11])
#        print(10, 10, c[10, 10])
#        print(10, 11, c[10, 11])
#        print(11, 10, c[11, 10])
#        print(11, 11, c[11, 11])
        res += c[pointsCnt, pointsCnt] * (pPoint ** 2) / (pPoint ** 2 + (1 - pPoint) ** 2)
#        print(res)
        return res

    #def predictTotal()
