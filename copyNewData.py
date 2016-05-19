from os import walk

def main():
    dirName = '2016-05-15'
    for f in walk('data/bkfon/live/new/' + dirName):
        for ff in f[2]:
            print(ff)

            with open('data/bkfon/live/new/'  + dirName + '/' + ff, 'r', encoding = 'utf-8') as fin, \
                 open('data/bkfon/live/' + ff, 'a', encoding = 'utf-8') as fout:
                for line in fin:
                    fout.write(line)

if __name__ == "__main__":
    main()