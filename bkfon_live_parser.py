from BKFonLiveParser import *
from BetsStorage import *
import json
from shutil import copyfile


def parseDirs(segments, segments1):
    dirname = 'data/bkfon/live'
    dirname_parsed = 'data/bkfon/live_parsed_new2'

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
        dirname_parsed_segment = dirname_parsed + '/' + segment
        if not os.path.exists(dirname_parsed_segment):
            os.mkdir(dirname_parsed_segment)

        parsed = list()
        if not os.path.exists(dirname_parsed_segment + '/' + 'parsed_filenames.txt'):
            open(dirname_parsed_segment + '/' + 'parsed_filenames.txt', 'w', encoding='utf-8').close()
        with open(dirname_parsed_segment + '/' + 'parsed_filenames.txt', encoding='utf-8') as fin:
            for line in fin:
                parsed.append(line.strip())

        if len(parsed) != 0 and os.path.exists(dirname_parsed_segment + '/' + parsed[-1].split('\\')[-2] + '.txt'):
            copyfile(dirname_parsed_segment + '/' + parsed[-1].split('\\')[-2] + '.txt',
                     dirname_parsed_segment + '/' + parsed[-1].split('\\')[-2] + '_last.txt')
            betsStorage.loadFromFile(dirname_parsed_segment + '/' + parsed[-1].split('\\')[-2] + '.txt', isPrepared=0)
            open(dirname_parsed_segment + '/' + parsed[-1].split('\\')[-2] + '.txt', 'w', encoding='utf-8').close()

        parsed = set(parsed)

        foutParsed = open(dirname_parsed_segment + '/' + 'parsed_filenames.txt', 'a', encoding='utf-8')

        for fname, fl in sorted(filenames, key=lambda x: x[0]):
            if fname in parsed:
                continue
            #if fname.find('2017-08-03') == -1:
            #    continue
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
            dateOutput = dict()
            for mKey, match in sorted(rows, key=lambda x: x[1].dt, reverse=0):
                # output only NOT live bets
                if mKey[0] != 'l':
                    continue
                matchDate = match.dt[:10]
                if matchDate not in dateOutput:
                    dateOutput[matchDate] = []
                dateOutput[matchDate].append('\t'.join([match.eventId, match.dt, match.compName,
                                             ';'.join(match.names[0]), ';'.join(match.names[1]),
                                             json.dumps(match.eventsInfo, ensure_ascii=False, sort_keys=True)]) + '\n')
                print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[0]])
                print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[-1]])

            for matchDate, outputList in dateOutput.items():
                with open(dirname_parsed_segment + '/' + matchDate + '.txt', 'a', encoding='utf-8') as fout:
                    for s in outputList:
                        fout.write(s)

            foutParsed.write(fname + '\n')

            # clean bets
            betsStorage.bets = dict()

        rows = list(betsStorage.bets.items()) + list(betsStorage.liveBets.items())
        dateOutput = dict()
        for mKey, match in sorted(rows, key=lambda x: x[1].dt, reverse=0):
            if mKey[0] != 'l':
                continue
            matchDate = match.dt[:10]
            if matchDate not in dateOutput:
                dateOutput[matchDate] = []
            dateOutput[matchDate].append('\t'.join([match.eventId, match.dt, match.compName,
                                         ';'.join(match.names[0]), ';'.join(match.names[1]),
                                         json.dumps(match.eventsInfo, ensure_ascii=False, sort_keys=True)]) + '\n')
            print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[0]])
            print([match.eventId, match.dt, match.compName, match.names, match.eventsInfo[-1]])

        for matchDate, outputList in dateOutput.items():
            with open(dirname_parsed_segment + '/' + matchDate + '.txt', 'a', encoding='utf-8') as fout:
                for s in outputList:
                    fout.write(s)


def my_debug():
    parser = BKFonLiveParserNew()
    betsStorage = BetsStorage()
    fname = r'C:\Programming\SportPrognoseSystem\TTStat\data\bkfon\live\2017-09-17\Наст. теннис. TT-CUP. Украина.txt'
    lastTime = None
    block = []
    with open(fname, 'r', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            if len(tokens) == 1:
                tokens = ['', tokens[0]]
            curTime = tokens[0]
            if curTime != lastTime and lastTime is not None:
                if curTime == '2017-09-17 11:06:59':
                    print(curTime)
                betsStorage.update(parser.addLineBlock(lastTime, block))
                block = []
            block.append(tokens[1])
            lastTime = curTime
        if lastTime is not None:
            betsStorage.update(parser.addLineBlock(lastTime, block))


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
    #мастер-тур Китай женщины - склеить
#    segments1['ittf'] = 'Международный турнир.'

    segments1['kchr'] = 'Континентальный чемпионат России'
    segments1['rus'] = 'Первенство России'

    #parseDirs(dict(), {'liga_pro_men': 'Наст. теннис. Лига Про. Москва.txt'})
    parseDirs(segments, segments1)

if __name__ == "__main__":
    main()