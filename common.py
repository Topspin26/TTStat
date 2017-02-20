
def readPlayers(filename, flAll = 0):
    players = dict()
    with open(filename, 'r', encoding = 'utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            id = tokens[0].strip()
            name = tokens[1].strip()
            players[id] = name.split(';')
            if flAll == 0:
                players[id] = players[id][0]
    return players

def readPlayersInv(filename):
    players = dict()
    players2 = dict()
    with open(filename, 'r', encoding = 'utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            id = tokens[0].strip()
            names = tokens[1].strip().split(';')
            for name in names:
                players[name] = id
                players[name.title()] = id
                tn = name.split(' ')
                if len(tn) > 1:
                    if name[0] >= 'A' and name[0] <= 'Z':
                        arr = [name, name.title(), tn[0], tn[0] + ' ' + ' '.join([(e[0] + '.') for e in tn[1:]]), tn[0] + ' ' + ' '.join([(e[0]) for e in tn[1:]])]
                    else:
                        arr = [name, name.title(), tn[1], tn[1] + ' ' + ' '.join([(e[0] + '.') for e in [tn[0]] + tn[2:]]), tn[1] + ' ' + ' '.join([(e[0]) for e in [tn[0]] + tn[2:]])]
                    if len(tn) == 2:
                        arr.append(tn[1] + ' ' + tn[0])
                else:
                    arr = [name]
                for short_player in arr:
                    if not (short_player in players2):
                        players2[short_player] = [id]
                    else:
                        players2[short_player].append(id)
                        players2[short_player] = list(set(players2[short_player]))
    return (players, players2)

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
