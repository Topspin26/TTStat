from os import walk
from lxml import html
from lxml import etree
import re
from Logger import Logger

monthname2Num = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'май': 5, 'мая': 5, 'июн': 6,
                 'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12}


class BKFonResultsParser:
    @staticmethod
    def run(logger=Logger()):
        print('BKFonResultsParser')
        logger.print('BKFonResultsParser')
        for f in walk('data/bkfon/results'):
            fSet = set(f[2])
            for ff in f[2]:
                # print(ff)
                if ff.find('old') != -1:
                    continue
                if ff.find('new') != -1:
                    if not (ff.replace('_new', '') in fSet):
                        sKey, lines = BKFonResultsParser.parse('data/bkfon/results/' + ff, logger, mode='new')
#            if ff.find('2016-11') == -1 and ff.find('2016-12') == -1 and ff.find('2017-') == -1:
#                continue
#            if ff.find('2017-02-07') == -1:
#                continue
                else:
                    sKey, lines = BKFonResultsParser.parse('data/bkfon/results/' + ff, logger, mode='old')
                logger.print(sKey)
                with open('data/bkfon/results_parsed/' + sKey + '.txt', 'w', encoding='utf-8') as fout:
                    fout.write(lines)

    @staticmethod
    def parse(filename, logger, mode='new'):
        if mode == 'new':
            return BKFonResultsParser.processNew(filename, logger)
        else:
            return BKFonResultsParser.processOld(filename, logger)

    @staticmethod
    def processNew(filename, logger):
        lines = []
        tid = filename.split('/')[-1][:-4]
        with open(filename, 'r', encoding='utf-8') as fin:
            for line in fin:
                table = html.fromstring(line)
                trs = table.xpath("//tr")
                logger.print(len(trs))
                compName = ''
                for itr, tr in enumerate(trs):
                    s = etree.tostring(tr, pretty_print=True, encoding='unicode')
                    if s.find('Нет событий') != -1:
                        continue
                    if tr.get('class').find('table__row _type_segment _sport_3088') != -1:
                        s = re.sub(r'\<\!--[^>]*--\>', '', s)
                        #print(s)
                        compName = s.split('"table__title-text">')[1].split('<')[0]
                        #print(compName)
                    else:
                        #if compName.find('TT-CUP') != -1:
                        #    continue
                        tds = tr.xpath('//tr[' + str(itr + 1) + ']/td')
                        s = re.sub(r'\<\!--[^>]*--\>', '', s)
                        #print(s.strip())
                        try:
                            timeArr = s.split('"table__time-icon')[1].split('<span>')[1].split('<')[0].split(' в ')
                        except:
                            logger.print(s)
                            raise
                        matchTime = timeArr[1]
                        try:
                            month = str(monthname2Num[timeArr[0].split()[1][:3]]).zfill(2)
                        except:
                            logger.print(timeArr)
                            continue
                        dt = tid[:4] + '-' + month + '-' + timeArr[0].split()[0].zfill(2)
                        #print(timeArr)
                        #print(dt)
                        names = s.split('"table__event-number">')[1].split('</span>')[1].split('<')[0].strip()

                        names = re.sub(' +', ' ', names.replace(u'\xa0', ' '))

                        names = names.strip().split(' - ')

                        matchId = s.split('"table__event-number">')[1].split('</span>')[0].strip()
                        #print(matchId)
                        setsScore = ''
                        try:
                            setsScore = s.split('"table__score">')[1].split('<')[0]
                        except:
                            pass
                        #print(setsScore)
                        pointsScore = ''
                        try:
                            pointsScore = s.split('"table__score-more">')[1].split('<')[0]
                            pointsScore = pointsScore.replace('(', '').replace(')', '').replace('\xa0', ';').replace('-', ':')
                        except:
                            pass
                        #print(pointsScore)

                        #if names[0].lower().find('game') != -1:
                        #    continue

                        lines.append('\t'.join([dt, matchTime, compName, matchId,
                                                ';'.join([e.strip() for e in names[0].strip().split('/')]),
                                                ';'.join([e.strip() for e in names[1].strip().split('/')]),
                                                setsScore, pointsScore]))
        return tid, '\n'.join(lines)

    @staticmethod
    def processOld(filename, logger):
        lines = []
        tid = filename.split('/')[-1][:-4]
        with open(filename, 'r', encoding='utf-8') as fin:
            for line in fin:
                table = html.fromstring(line)
                trs = table.xpath("*//tr")
                flTT = 0
                compName = ''
                for tr in trs:
                    if tr.get('class') == 'sectCaption':
                        s = tr.xpath('.//th/text()')[0].replace(u'\xa0', ' ')
                        compName = s
                        if s.find('Наст. теннис') != -1 and s.find('TT-CUP') == -1:
                            flTT = 1
                            # print(s)
                        else:
                            flTT = 0
                    else:
                        if flTT == 1:
                            arr = [re.sub(' +', ' ', e.replace(u'\xa0', ' ')) for e in tr.xpath('.//text()')]

                            #print(arr)
                            timeArr = arr[1].split(' ')
                            if len(timeArr) == 2:
                                time = timeArr[1].strip()
                            else:
                                time = timeArr[0].strip()

                            matchTime = time

                            dt = timeArr[0].strip()
                            if len(dt.split('.')) == 2:
                                day = dt.split('.')[0].zfill(2)
                                month = dt.split('.')[1].zfill(2)
                                year = tid[:4]
                                dt = year + '-' + month + '-' + day
                            else:
                                dt = tid[:10]

                            arr = [e.replace('(ж)', '') for e in arr]
                            s0 = '\t'.join(arr)

                            names = arr[2].strip().split(' - ')
                            if len(names) != 2:
                                logger.print(arr)
                                continue
#                            if names[0].lower().find('game') != -1:
#                                continue
#                                if dt != ff[:10]:
#                                    print(dt + ' ' + ff[:10])
                            matchId = arr[0]
                            setsScore = arr[3]
                            pointsScore = arr[4].replace('(', '').replace(')', '').replace(' ', ';').replace('-', ':')
                            lines.append('\t'.join([dt, matchTime, compName, matchId,
                                                    ';'.join([e.strip() for e in names[0].strip().split('/')]),
                                                    ';'.join([e.strip() for e in names[1].strip().split('/')]),
                                                    setsScore, pointsScore]))
#                            if arr[4] != 'отмена':
        return tid, '\n'.join(lines)

def main():
    #BKFonResultsParser.processNew('data/bkfon/results/2017-07-05_new.txt')
    BKFonResultsParser.run(logger=Logger('BKFonResultsParser.txt'))

if __name__ == "__main__":
    main()
