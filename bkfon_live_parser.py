from BKFonLiveParser import *
from BetsStorage import *
import json

def parseDirs(segments, segments1):
    dirname = 'data/bkfon/live'
    dirname_parsed = 'data/bkfon/live_parsed_new'

    segmentFilenames = dict()
    for f in walk(dirname):
        for ff in f[2]:
            fp = os.path.abspath(os.path.join(f[0], ff))
            if fp.find('undefined') != -1 or fp.find('error') != -1:
                continue
            fl = 0
            for segment in segments:
                if fp.find(segments[segment]) != -1:
                    if segment not in segmentFilenames:
                        segmentFilenames[segment] = []
                    segmentFilenames[segment].append([fp, 'old'])
                    fl = 1
                    break
            if fl == 0:
                for segment in segments1:
                    if fp.find(segments1[segment]) != -1:
                        if segment not in segmentFilenames:
                            segmentFilenames[segment] = []
                        segmentFilenames[segment].append([fp, 'new'])
                        fl = 1
                        break
            if fl == 0:
                segment = ff[:-4]
                if segment not in segmentFilenames:
                    segmentFilenames[segment] = []
                if fp.find('segment') != -1:
                    segmentFilenames[segment].append([fp, 'old'])
                else:
                    segmentFilenames[segment].append([fp, 'new'])

    for segment, filenames in sorted(segmentFilenames.items(), key=lambda x: -len(x[1])):
        print(segment, len(filenames), filenames)
        parserOld = BKFonParser()
        parserNew = BKFonLiveParserNew()
        betsStorage = BetsStorage()
        if os.path.exists(dirname_parsed + '/' + segment + '.txt'):
            continue
        with open(dirname_parsed + '/' + segment + '.txt', 'w', encoding='utf-8') as fout:
            for fname, fl in sorted(filenames, key=lambda x: x[0]):
                parser = parserNew if fl == 'new' else parserOld
                print(fname)
                lastTime = None
                block = []
                with open(fname, 'r', encoding='utf-8') as fin:
                    for line in fin:
                        tokens = line.split('\t')
                        if len(tokens) == 1:
                            tokens = ['', tokens[0]]
                        curTime = tokens[0]
                        if curTime != lastTime and lastTime is not None:
                            betsStorage.update(parser.addLineBlock(lastTime, block))
                            block = []
                        block.append(tokens[1])
                        lastTime = curTime
                    if lastTime is not None:
                        betsStorage.update(parser.addLineBlock(lastTime, block))
                #break
                rows = list(betsStorage.bets.items())
                for mKey, match in sorted(rows, key=lambda x: x[1].dt, reverse=0):
                    if mKey[0] != 'l':
                        continue
                    fout.write('\t'.join([match.eventId, match.dt, match.compName,
                                          ';'.join(match.names[0]), ';'.join(match.names[1]),
                                          json.dumps(match.eventsInfo, ensure_ascii=False)]) + '\n')
                    print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[0]])
                    print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[-1]])
                betsStorage.bets = dict()

            rows = list(betsStorage.liveBets.items())
            for mKey, match in sorted(rows, key=lambda x: x[1].dt, reverse=0):
                if mKey[0] != 'l':
                    continue
                fout.write('\t'.join([match.eventId, match.dt, match.compName,
                                      ';'.join(match.names[0]), ';'.join(match.names[1]),
                                      json.dumps(match.eventsInfo, ensure_ascii=False)]) + '\n')
                print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[0]])
                print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[-1]])

def main():
    segments = dict()

    segments['master_tour_mix'] = 'segment28824.txt'
    segments['master_tour_women'] = 'segment25827.txt'  # + CHINA!?
    segments['master_tour_men_spb'] = 'segment26989.txt'
    segments['master_tour_men_isr'] = 'segment30240.txt'
    segments['master_tour_women_chn'] = 'segment18054.txt'
    segments['master_tour_men_chn'] = 'segment34654.txt'

    segments['liga_pro_men'] = 'segment37716.txt'
    segments['liga_pro_women'] = 'segment37984.txt'
    segments['challenger_series_men'] = 'segment13574.txt'
    segments['challenger_series_women'] = 'segment19423.txt'

    segments1 = dict()
    segments1['liga_pro_men'] = 'Наст. теннис. Лига Про. Москва.txt'
    segments1['liga_pro_women'] = 'Наст. теннис. Жен. Лига Про. Москва.txt'
    segments1['challenger_series_men'] = 'Наст. теннис. Челленджер серия.txt'
    segments1['challenger_series_women'] = 'Наст. теннис. Жен. Челленджер серия.txt'
    segments1['master_tour_men_spb'] = 'Наст. теннис. Мастер-Тур. С-Петербург.txt'
    segments1['master_tour_women'] = 'Наст. теннис. Жен. Мастер-Тур. С-Петербург.txt'
    segments1['master_tour_men_isr'] = 'Наст. теннис. Мастер-Тур. Израиль.txt'
#    segments1['ittf'] = 'Международный турнир.'

    parseDirs(segments, segments1)

    dirname_parsed = 'data/bkfon/live_parsed_new'

if __name__ == "__main__":
    main()