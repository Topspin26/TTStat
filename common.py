from selenium import webdriver
import time
import hashlib


def initDriver(url, sleepTime=0, port=5938):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port=port)
    driver.get(url)
    time.sleep(sleepTime)
    return driver


def calcHash(arr):
    res = 0
    for e in arr:
        res ^= int(hashlib.md5(str(e).encode()).hexdigest(), 16)
    res = (res // (1 << 32)) ^ (res % (1 << 32))
    return str(res)


class GlobalPlayersDict:
    def __init__(self, mode=None, dirname=''):
        if mode == 'filtered':
            import filterPlayersByRusRanking
            filterPlayersByRusRanking.main()
        self.name2id = dict()
        self.name2id2 = dict()
        self.id2names = dict()
        if mode is None:
            self.filenames = {'m': dirname + 'prepared_data/players_men.txt',
                              'w': dirname + 'prepared_data/players_women.txt'}
        elif mode == 'filtered':
            self.filenames = {'m': dirname + 'prepared_data/players_men_filtered.txt',
                              'w': dirname + 'prepared_data/players_women_filtered.txt'}
        for mw in ['m', 'w']:
            with open(self.filenames[mw], 'r', encoding='utf-8') as fin:
                for line in fin:
                    tokens = line.split('\t')
                    id = tokens[0].strip()
                    names = tokens[1].strip().split(';')
                    if id in self.id2names:
                        print(id)
                        raise
                    self.setId2Names(id, names)

    def setId2Names(self, id, names):
        self.id2names[id] = names
        self.updateInv(id)

    def updateInv(self, id):
        names = self.id2names[id]
        for name in names:
            name = name.lower().replace('ё', 'е')
            name_tokens = name.split(' ')
            name1 = ' '.join(name_tokens[1:]) + ' ' + name_tokens[0]
            for tname in [name, name1]:
                if self.name2id.get(tname, id) != id:
                    print('Bad name ' + tname + ' ' + self.name2id.get(tname, id) + ' ' + id)
                    if not (tname in {'yang ying', 'ying yang',\
                                      'li xiang', 'xiang li',\
                                      'yang min', 'min yang',\
                                      'денис макаров', 'макаров денис',\
                                      'иван архипов', 'архипов иван',\
                                      'дмитрий осипов', 'осипов дмитрий',
                                      'анастасия голубева', 'голубева анастасия',
                                      'александр козлов', 'козлов александр',
                                      'олег попов', 'попов олег'}):
                        raise
                self.name2id[tname] = id

            tn = name.split(' ')
            tn1 = name1.split(' ')
            if len(tn) > 1:
                if 'a' <= name[0] <= 'z':
                    arr = [name, name1, tn[0], tn1[0],
                           tn[0] + ' ' + ' '.join([(e[0] + '.') for e in tn[1:]]),
                           tn[0] + ' ' + ' '.join([(e[0]) for e in tn[1:]]),
                           tn1[0] + ' ' + ' '.join([(e[0] + '.') for e in tn1[1:]]),
                           tn1[0] + ' ' + ' '.join([(e[0]) for e in tn1[1:]])]
                else:
                    arr = [name, name1, tn[1], tn1[1],
                           tn[1] + ' ' + ' '.join([(e[0] + '.') for e in [tn[0]] + tn[2:]]),
                           tn[1] + ' ' + ' '.join([(e[0]) for e in [tn[0]] + tn[2:]]),
                           tn[-1] + ' ' + ' '.join([(e[0]) for e in tn[:-1]]),
                           tn[-1] + ' ' + ' '.join([(e[0] + '.') for e in tn[:-1]]),
                           tn1[-1] + ' ' + ' '.join([(e[0] + '.') for e in tn1[:-1]]),
                           tn1[-1] + ' ' + ' '.join([(e[0]) for e in tn1[:-1]]),
                           tn1[1] + ' ' + ' '.join([(e[0] + '.') for e in [tn1[0]] + tn1[2:]]),
                           tn1[1] + ' ' + ' '.join([(e[0]) for e in [tn1[0]] + tn1[2:]])]
                    if tn[0] == 'александр':
                        arr += [tn[1] + ' ал-р', 'ал-р ' + tn[1]]
                    elif tn[1] == 'александр':
                        arr += [tn[0] + ' ал-р', 'ал-р ' + tn[0]]
                    if tn[0] == 'алексей':
                        arr += [tn[1] + ' ал-й', 'ал-й ' + tn[1]]
                    elif tn[1] == 'алексей':
                        arr += [tn[0] + ' ал-й', 'ал-й ' + tn[0]]
            else:
                arr = [name]
            for short_player in arr:
                short_player = short_player.lower()
                if not (short_player in self.name2id2):
                    self.name2id2[short_player] = [id]
                else:
                    self.name2id2[short_player].append(id)
                    self.name2id2[short_player] = list(set(self.name2id2[short_player]))

    def getId(self, name, fl=1):
        name = name.lower().replace('ё', 'е').replace('ö', 'o').replace('^', '').replace(',', '').strip()
        name = ' '.join(name.split())
        if len(name) > 0 and not ('a' <= name[0] <= 'z'):
            name = name.replace('c', 'с') #russian c
        if fl == 1:
            return self.name2id2.get(name, [])
        return self.name2id.get(name, None)

    def getName(self, playerId, fl=0):
        if fl == 0:
            return self.id2names[playerId][0]
        return self.id2names.get(playerId, [None])[0]

    def getNames(self, playerId):
        return self.id2names[playerId]

    def getMaxId(self, mw):
        res = 0
        for e in self.id2names:
            if e[0] == mw:
                res = max(res, int(e[1:]))
        return res

    def updateId2names(self, id, name):
        name = name.replace('ё', 'е').replace('Ё', 'Е').replace('ö', 'o')
        if self.getId(name, 0) is None:
            self.setId2Names(id, self.id2names[id] + [name])


def updateDict(d, k, val=1):
    if k in d:
        d[k] += val
    else:
        d[k] = val

def readCorrections(filename):
    corrections = dict()
    with open(filename, 'r', encoding = 'utf-8') as fin:
        lastLine = None
        for i, line in enumerate(fin):
            if i % 2 == 1:
                corrections[lastLine.strip()] = line.strip()
            lastLine = line
    return corrections

def readCorrectionsList(filename):
    corrections = []
    with open(filename, 'r', encoding = 'utf-8') as fin:
        lastLine = None
        for i, line in enumerate(fin):
            if i % 2 == 1:
                corrections.append([lastLine.strip(), line.strip()])
            lastLine = line
    return corrections

def readPlayer2Id(filename):
    player2id = dict()
    id2player = dict()
    with open(filename, encoding = 'utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            if len(tokens[1].strip()) > 0:
                player2id[tokens[0]] = tokens[1].strip().split(';')
                id2player[tokens[1].strip()] = tokens[0]
            else:
                print('ERROR')
                print(line)
                raise

    return [player2id, id2player]