import liga_pro_prepare
import master_tour_prepare
import challenger_series_prepare
import bkfon_results_prepare
import ittf_prepare
import kchr_prepare
import propingpong_prepare
import rttf_prepare

from common import *
from Entity import *

def prepareSources():
    master_tour_prepare.main()
    liga_pro_prepare.main()
    challenger_series_prepare.main()
    bkfon_results_prepare.main()
    propingpong_prepare.main()
    ittf_prepare.main()
    kchr_prepare.main()
    rttf_prepare.main()

def main():
    prepareSources()

    sources = []
    sources.append(['master_tour', r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\master_tour\all_results.txt'])
    sources.append(['liga_pro', r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\liga_pro\all_results.txt'])
    sources.append(['challenger_series',r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\challenger_series\all_results.txt'])
    sources.append(['bkfon', r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\bkfon\all_results.txt'])
    sources.append(['local', r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\local\kchr_results.txt'])
    sources.append(['ittf', r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\ittf\all_results.txt'])
    sources.append(['rttf', r'D:\Programming\SportPrognoseSystem\BetsWinner\prepared_data\rttf\all_results.txt'])

    matchesDict = dict()

    with open('prepared_data/matches_hashes.txt', 'w', encoding = 'utf-8') as fout:
        for source, filename in sources:
            print(filename)
            with open(filename, encoding='utf-8') as fin:
                headerTokens = next(fin).strip().split('\t')
                headerDict = dict(zip(headerTokens, range(len(headerTokens))))
                for line in fin:
                    tokens = line.split('\t')
                    match = Match(tokens[headerDict['date']],
                                  [tokens[headerDict['id1']].split(';'), tokens[headerDict['id2']].split(';')],
                                  setsScore=tokens[headerDict['setsScore']],
                                  pointsScore=tokens[headerDict['pointsScore']],
                                  time=tokens[headerDict['time']],
                                  compName=tokens[headerDict['compName']],
                                  source=source)
                    matchHash = match.getHash()
                    if not (matchHash in matchesDict):
                        matchesDict[matchHash] = match
                    else:
                        if source != 'bkfon' and not ('bkfon' in matchesDict[matchHash].sources):
                            fout.write(';'.join(matchesDict[matchHash].sources) + '\t' + matchesDict[matchHash].toStr() + '\n')
                            fout.write(source + '\t' + match.toStr() + '\n')
                            fout.write('\n')
                            print([matchesDict[matchHash].toStr(), match.toStr()])

if __name__ == "__main__":
    main()