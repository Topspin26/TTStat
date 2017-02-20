import time
import os
from lxml import html
from lxml import etree
import datetime as datetime

def main():
    dir = 'D:/Programming/SportPrognoseSystem/BetsWinner/data/bkfon/live'

    for f in os.listdir(dir + '/old'):
        if f[:7] == 'segment':
            print(f)
            with open(dir + '/old/' + f, 'r', encoding='utf-8') as filename:
                fout = None
                k = 0
                lastDt = None
                for line in filename:
                    tokens = line.split('\t')
                    dt = 'undefined'
                    if len(tokens) == 2:
                        dt = (datetime.datetime.strptime(tokens[0], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
#                        print((tokens[0], dt))
                        tokens[0] = dt
                        dt = dt[:10]
                    if dt != lastDt:
                        if not (fout is None):
                            fout.close()
                        if not os.path.exists(dir + '/' + dt):
                            os.mkdir(dir + '/' + dt)
                        fout = open(dir + '/' + dt + '/' + f[:-4] + '.txt', 'w', encoding = 'utf-8')
                    fout.write('\t'.join(tokens))
                    lastDt = dt
            if not (fout is None):
                fout.close()
#            break

if __name__ == "__main__":
    main()