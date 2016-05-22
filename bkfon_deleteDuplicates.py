import time
import os
from lxml import html
from lxml import etree

def main():
    dir = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live'

    for f in os.listdir(dir):
#        print(os.path.isfile(os.path.join(dir, f)))
        if f[:7] == 'segment':
            trSegmentLine = None
            trEventLines = None
            trEventS = None
            lastEventId = None
            eventsDict = dict()
            print(f)
            with open(dir + '/' + f, 'r', encoding='utf-8') as filename, \
                 open(dir + '/clean/' + f, 'w', encoding='utf-8') as fout:
                k = 0
                for line in filename:
                    tokens = line.split('\t')
                    time = ''
                    if len(tokens) == 2:
                        time = tokens[0]
                        s = tokens[1]
                    else:
                        s = line
                    tr = html.fromstring(s)
                    cl = tr.get('class')
                    
                    if cl.find('trEventChild') == -1:
                        if not (lastEventId is None):
                            printFl = 1
                            if lastEventId in eventsDict:
                                if eventsDict[lastEventId] == trEventS:
                                    printFl = 0
                            if printFl == 1:
                                if trSegmentLine != '':
                                    fout.write(trSegmentLine)
                                    trSegmentLine = ''
                                fout.write(trEventLines)
                            eventsDict[lastEventId] = trEventS
                        if cl != 'trSegment':
                            lastEventId = tr.get('id')
                        else:
                            lastEventId = None
                        trEventLines = ''
                        trEventS = ''
                    
                    if cl == 'trSegment':
                        trSegmentLine = line
                    else:
                        trEventLines += line
                        trEventS += s
                    
                    k += 1
                    if k % 1000 == 0:
                        print(k)
#                        if k == 2000:
#                            break
                if not (lastEventId is None):
                    printFl = 1
                    if lastEventId in eventsDict:
                        if eventsDict[lastEventId] == trEventS:
                            printFl = 0
                    if printFl == 1:
                        if trSegmentLine != '':
                            fout.write(trSegmentLine)
                        fout.write(trEventLines)

if __name__ == "__main__":
    main()