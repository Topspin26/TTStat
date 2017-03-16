from selenium import webdriver
import time

def initDriver(url, sleepTime = 0, port = 5938):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = port)
    driver.get(url)
    time.sleep(sleepTime)
    return driver

class GlobalPlayersDict():
    def __init__(self):
        self.name2id = dict()
        self.name2id2 = dict()
        self.id2names = dict()
        filenames = {'m': r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_men.txt',
                     'w': r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\players_women.txt'}
        for mw in ['m', 'w']:
            with open(filenames[mw], 'r', encoding='utf-8') as fin:
                for line in fin:
                    tokens = line.split('\t')
                    id = tokens[0].strip()
                    names = tokens[1].strip().split(';')
                    if id in self.id2names:
                        print(id)
                        raise
                    self.id2names[id] = names
                    for name in names:
                        name = name.replace('ё', 'е').lower()
                        if self.name2id.get(name, id) != id:
                            print('Bad name ' + name)
                            if not (name in {'yang ying', 'li xiang'}):
                                raise
                        self.name2id[name] = id
                        tn = name.split(' ')
                        if len(tn) > 1:
                            if name[0] >= 'a' and name[0] <= 'z':
                                arr = [name, name.title(), tn[0],
                                       tn[0] + ' ' + ' '.join([(e[0] + '.') for e in tn[1:]]),
                                       tn[0] + ' ' + ' '.join([(e[0]) for e in tn[1:]])]
                            else:
                                arr = [name, name.title(), tn[1], tn[1] + ' ' + ' '.join([(e[0] + '.') for e in [tn[0]] + tn[2:]]),
                                       tn[1] + ' ' + ' '.join([(e[0]) for e in [tn[0]] + tn[2:]])]
                            if len(tn) == 2:
                                arr.append(tn[1] + ' ' + tn[0])
                        else:
                            arr = [name]
                        for short_player in arr:
                            short_player = short_player.lower()
                            if not (short_player in self.name2id2):
                                self.name2id2[short_player] = [id]
                            else:
                                self.name2id2[short_player].append(id)
                                self.name2id2[short_player] = list(set(self.name2id2[short_player]))

    def getId(self, name):
        name = name.lower().replace('ё', 'е').replace('^', '').replace(',', '').strip()
        return self.name2id2.get(name, [])
    def getName(self, id):
        return self.id2names[id][0]
    def getNames(self, id):
        return self.id2names[id]

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
