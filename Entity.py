
class MatchBet:
    def __init__(self, eventId, rows, dt, compName, players, score, bet_win):
        self.eventId = eventId
        self.rows = rows
        self.dt = dt
        self.compName = compName
        self.players = players
        self.score = score
        self.bet_win = bet_win
 
class Player:
    def __init__(self, id, name, mw):
        self.id = id
        self.name = name
        self.mw = mw
        self.matches = []

class Match:
    '''
    def __init__(self, date, isPair, players, wins, sets, setsScore, time = '12:00', points = [-1, -1], pointsScore = ''):
        self.date = date
        self.time = time
        self.isPair = isPair
        self.players = players
        self.wins = wins
        self.sets = sets
        self.setsScore = setsScore
        self.points = points
        self.pointsScore = pointsScore
    '''

    def __init__(self, date, players, winsScore = None, setsScore = None, pointsScore=None,
                 time=None, isPair = None, compName = None):
        self.date = date
        self.players = players
        self.flError = 0

        self.winsScore = winsScore
        self.wins = None
        self.setsScore = setsScore
        self.sets = None
        self.pointsScore = pointsScore
        self.points = None

        if (self.setsScore is None) and not (self.pointsScore is None):
            self.sets, self.points = Match.getPointsScoreInfo(self.pointsScore)
            self.setsScore = str(self.sets[0]) + ':' + str(self.sets[1])
        if not (self.setsScore is None) and (self.sets is None):
            try:
                self.sets = [int(e) for e in self.setsScore.split(':')]
            except:
                self.flError = 1
                pass
        if not (self.pointsScore is None) and (self.points is None):
            try:
                _, self.points = Match.getPointsScoreInfo(self.pointsScore)
            except:
                self.flError = 1
                pass

        if (self.winsScore is None) and not (self.sets is None):
            self.wins = [int(self.sets[0] > self.sets[1]), int(self.sets[1] > self.sets[0])]
            self.winsScore = str(self.wins[0]) + ':' + str(self.wins[1])
        if not (self.winsScore is None) and (self.wins is None):
            self.wins = [int(e) for e in self.winsScore.split(':')]

        self.compName = compName
        self.time = time
        self.isPair = isPair
        if (self.isPair is None):
            if len(self.players[0]) == 2:
                self.isPair = 1

    def toStr(self):
        return '\t'.join([self.date, self.time, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]), self.setsScore, self.pointsScore])
    def toArr(self):
        return [self.date, self.time, self.compName, ';'.join(self.players[0]), ';'.join(self.players[1]), self.setsScore, self.pointsScore]

    @staticmethod
    def getPointsScoreInfo(pointsScore):
        sets = [0, 0]
        points = [[],[]]
        for e in pointsScore.replace(':;', '').strip().strip(';').split(';'):
            if e == ':':
                continue
            try:
                tt = e.split(':')
                p1 = int(tt[0])
                points[0].append(p1)
                p2 = int(tt[1])
                points[1].append(p2)
                sets[0] += int(p1 > p2)
                sets[1] += int(p2 > p1)
            except Exception as ex:
                print(pointsScore)
                raise
        return [sets, points]

    @staticmethod
    def checkSetScore(score):
        tt = score.split(':')
        res = True
        try:
            set1 = int(tt[0])
            set2 = int(tt[1])
            if min(set1, set2) < 0 or max(set1, set2) < 11:
                res = False
            if max(set1, set2) == 11:
                if min(set1, set2) > 9:
                    res = False
            else:
                if max(set1, set2) - min(set1, set2) != 2:
                    res = False
        except:
            res = False
        return res

    @staticmethod
    def checkSetsScore(score):
        res = score in {'3:0', '3:1', '3:2', '2:3', '1:3', '0:3',
                        '4:0', '4:1', '4:2', '4:3', '3:4', '2:4', '1:4', '0:4'}
        return res

    def getSumPoints(self):
        return [sum(self.points[0]), sum(self.points[1])]

    def getTotalPoints(self):
        return sum(self.points[0]) + sum(self.points[1])


