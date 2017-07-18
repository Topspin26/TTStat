import LigaProPreparator
import MasterTourPreparator
import ChallengerSeriesPreparator
import BKFonResultsPreparator
import IttfPreparator
import kchr_prepare
import propingpong_prepare
import RttfPreparator

from common import *
from Entity import *

def prepareSources():
    MasterTourPreparator.main()
    LigaProPreparator.main()
    ChallengerSeriesPreparator.main()
    BKFonResultsPreparator.main()
    propingpong_prepare.main()
    IttfPreparator.main()
    kchr_prepare.main()
    RttfPreparator.main()

def main():
    prepareSources()

    sources = []
    sources.append(['master_tour', 'prepared_data/master_tour/all_results.txt'])
    sources.append(['liga_pro', 'prepared_data/liga_pro/all_results.txt'])
    sources.append(['challenger_series', 'prepared_data/challenger_series/all_results.txt'])
    sources.append(['bkfon', 'prepared_data/bkfon/all_results.txt'])
    sources.append(['local', 'prepared_data/local/kchr_results.txt'])
    sources.append(['ittf', 'prepared_data/ittf/all_results.txt'])
    sources.append(['rttf', 'prepared_data/rttf/all_results.txt'])

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