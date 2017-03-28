import time
import random
import os
from os import walk
import datetime as datetime

from Entity import *
from common import *


def main():
    dir = 'D:/Programming/SportPrognoseSystem/Результаты/КЧР'

    fout = open('prepared_data/local/kchr_results.txt', 'w', encoding = 'utf-8')
    fout.write('\t'.join(['date','time','compName','id1','id2','setsScore','pointsScore','name1','name2']))

    monthname2Num = {'января':1,'февраля':2,'марта':3,'апреля':4,'мая':5,'июня':6,'июля':7,'августа':8,'сентября':9,'октября':10,'ноября':11,'декабря':12}

    rs = {'A', 'B', 'C', 'А', 'В', 'С', 'A/D', 'B/D', 'па-ра', 'Па-ра', 'A1', 'А1', 'A2', 'А2', 'A3', 'А3', 'A1/A4', 'А1/А4', 'A2/A4', 'А2/А4',
          '1/A4', '1/А4', '2/A4', '2/А4', 'X/W', 'Х/W', 'Y/W',
          'X', 'X', 'Y', 'Z', 'B1', 'B2', 'B3', 'В1', 'В2', 'В3', '1/В4', '1/B4', '2/В4', '2/B4', 'В1/В4', 'B1/B4', 'В2/В4', 'B2/B4'}

    corrections = readCorrections('data/local/kchr_corrections.txt')
#    print(corrections)


    playersDict = GlobalPlayersDict()

    compInfo = dict()
    with open('data/local/kchr_dates.txt', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.rstrip().split('\t')
            compInfo[tokens[0]] = tokens[1:]

    unknown = dict()
    namesCorr = {'БЕСЧАСНЫЙ Юрий': 'БЕСЧАСТНЫЙ Юрий',
                 'Азренкова Дарья':'Азаренкова Дарья',
                 'САЕРХАНОВ Руслан':'САМЕРХАНОВ Руслан',
                 'АПАГУНИ Эдард':'АПАГУНИ Эдуард',
                 'УРАЗОВ Святослв':'УРАЗОВ Святослав',
                 'КУЗНЕЦОВ Констнтин':'КУЗНЕЦОВ Константин',
                 'АРТЕМНКО Никита':'АРТЕМЕНКО Никита',
                 'ЕВСЕВ Ярослав':'ЕВСЕЕВ Ярослав',
                 'ГАЛЛЕВА Алсу':'ГАЛЕЕВА Алсу',
                 'МОВСИЯН Карен':'МОВСИСЯН Карен',
                 'КРАСКОВСКИЙ Алесандр':'КРАСКОВСКИЙ Александр',
                 'СОФРОНОВА Александр':'СОФРОНОВА Александра',
                 'ДОРОФЕЕВ Алксей':'ДОРОФЕЕВ Алексей',
                 'КОТЕЛЬНИКОВ Ксения':'КОТЕЛЬНИКОВА Ксения',
                 'БАЛАНЧУК Никлай':'БАЛАНЧУК Николай',
                 'ГРИШЕНИЕ Денис':'ГРИШЕНИН Денис',
                 'КРЕГЕЛЬ Дитрий':'КРЕГЕЛЬ Дмитрий',
                 'ВЕРЕВКИА Алла': 'ВЕРЕВКИНА Алла'}

    multiple = dict()
    unknown = dict()

    for f in walk(dir):
        for ff in f[2]:
            fp = os.path.abspath(os.path.join(f[0], ff))
            if fp[-3:] == 'pdf':
                continue
            #print(fp)
            cm = 0
            cmg = 0
            cp = cpg = 0
            matches = []
            compName = ', '.join(fp.split('\\')[-4:-1]).replace('women', 'Женщины').replace('men', 'Мужчины')
            with open(fp, encoding='utf-8') as fin, open('data/local/errors/' + '_'.join(fp.split('\\')[-5:])[:-4] + '_err.txt', 'w', encoding='utf-8') as fout_err:
                compDate = compInfo['/'.join(fp.split('\\')[-5:])][0]
                compDate = compDate.split(' ')[2] + '-' + str(monthname2Num[compDate.split(' ')[1]]).zfill(2) + '-' + compDate.split(' ')[0].split('-')[1].zfill(2)
                compDate = (datetime.datetime.strptime(compDate, "%Y-%m-%d").date() + datetime.timedelta(days=0)).strftime("%Y-%m-%d")
                compPlace = compInfo['/'.join(fp.split('\\')[-5:])][1]
                for line in fin:
                    line0 = line
                    if line.replace('\t', ';').strip() in corrections:
                        line = corrections[line.replace('\t', ';').strip()].replace(';', '\t')
#                        print(line)
#                        return
                    for e in ['X', 'Y', 'Z', 'В1', 'В2', 'В3']:#, '3 - 0', '3 - 1', '3 - 2', '2 - 3', '1 - 3', '0 - 3']:
                        line = line.replace(' ' + e + ' ', '\t' + e + '\t')
                        line = line.replace('\t' + e + ' ', '\t' + e + '\t')
                    for e in rs:
                        line = line.replace(e + '\t\t', e + '\t')
                        line = line.replace(e + '\t\t', e + '\t')
                        line = line.replace(e + '\t\t', e + '\t')
                    line = '\t' + line.replace('"', '').replace('\tv', '').replace('\tV', '').replace('v', '').replace('V', '').replace('\t\t\t\t', '\t').strip().replace(' \t', '\t')
                    line = line.replace('\t\t\t', '\t')
                    for e in rs:
                        line = line.replace('\t' + e + ' ', '\t' + e + '\t')
                    line = line.strip()
                    tokens = line.split('\t')
                    if tokens[0].lower() == 'па-':
                        line = line.replace('"', '').strip() + next(fin).replace('"', '').strip()
                        if line.replace('"', '').strip().split('\t')[0] in {'па-ра', 'Па-ра'}:
                            line += '_' + \
                               next(fin).replace('"', '').strip() + next(fin).replace('"', '').strip() + '_' + \
                               next(fin).replace('"', '').strip()
                        tokens = line.replace('"', '').strip().split('\t')
                        #print(tokens)
                        #print(line)
#                    if fp.split('\\')[-1] == 'tabula-16.05-mpr.3tur.1gr-1.tsv':
#                        print(tokens)
#                    if fp.split('\\')[-1] == 'tabula-3-i-tur-muzhchiny.-super.-1-gr.tsv':
#                        print('_________________________________' + str(tokens))
#                    else:
#                        continue

                    if tokens[0] in rs and len(tokens) > 6 and len(tokens[1]) > 0:
                        if (len(tokens[-1].replace(' ', '')) < 3 or tokens[-1].find('-') != -1 or tokens[-1].find(':') != -1)  and tokens[-1] != 'V':
                            name1 = tokens[1].replace('  ', ' ').split('_')
                            name2 = tokens[3].replace('  ', ' ').split('_')
                            if not (tokens[2] in rs):
                                name2 = tokens[4].split('_')
                            if tokens[-1] in {'0', '1'} and tokens[-2] in {'0', '1'} and \
                                tokens[-3] in {'3 0','3 1','3 2','2 3','1 3','0 3'}:
                                tokens = tokens[:-3] + tokens[-3].split(' ') + tokens[-2:]
                            if tokens[-1] in {'0', '1'} and tokens[-2] in {'0 3 0', '1 3 0', '2 3 0', '3 2 1', '3 1 1', '3 0 1'}:
                                tokens = tokens[:-2] + tokens[-2].split(' ')[:2] + [tokens[-2][-1], tokens[-1]]

                            setsScore = tokens[-4] + ':' + tokens[-3]

                            if fp.split('\\')[-1] == 'tabula-1-3muzh-kchr-premer.1-tur-1-moskva.tsv':
                                setsScore = tokens[-2].replace(' ', '').replace('-', ':')
                            elif fp.split('\\')[-1] in ['tabula-a-muzhchiny-1t-1-gr.tsv', 'tabula-superliga.zhenshch.-2-1-i-tur.tsv',
                                                        'tabula-2016-06-05-01-kch-premer-zh-gr-1-2-slavyansk.tsv', 'tabula-2015-11-08-kch-fntr-premer-liga-zhenshchiny-1-gruppa.tsv',
                                                        'tabula-2016-17.-1-t.-m-c.-1-gr.tsv']:
                                setsScore = tokens[-2]
                            elif tokens[-2].find(' ') != -1:
                                setsScore = tokens[-2].replace(' ', ':')

                            name1 = [namesCorr.get(e.replace(',', ''), e) for e in name1]
                            name2 = [namesCorr.get(e.replace(',', ''), e) for e in name2]
                            flError = 0
                            ids = [[], []]
                            names = [name1, name2]
                            for i in range(2):
                                for name in names[i]:
                                    player = ''.join([i for i in name if not i.isdigit()])
                                    id = playersDict.getId(player)

                                    if len(id) == 1:
                                        ids[i].append(id[0])
                                    elif len(id) == 0:
                                        flError = 1
                                        if not (player in unknown):
                                            unknown[player] = 0
                                        unknown[player] += 1
                                        fout_err.write('UNKNOWN ' + player + '\n')
                                        #print('UNKNOWN ' + player)
                                        if player == '':
                                            fout_err.write('-------------------' + line0 + '\n')
                                            #print('-------------------' + line0)
                                    else:
                                        flError = 1
                                        fout_err.write('MULTIPLE ' + player + '\n')
                                        #print('MULTIPLE ' + player)
                                        fl_mw = ''
                                        for e in id:
                                            fl_mw += e[0]
                                        fl_mw = ''.join(sorted(set(list(fl_mw))))
                                        if not (fl_mw + ' ' + player in multiple):
                                            multiple[fl_mw + ' ' + player] = 0
                                        multiple[fl_mw + ' ' + player] += 1

                            name1 = [''.join([i for i in name if not i.isdigit()]).strip().title().replace('ё','е').replace(',', '') for name in name1]
                            name2 = [''.join([i for i in name if not i.isdigit()]).strip().title().replace('ё','е').replace(',', '') for name in name2]
                            if flError == 0:
                                matches.append(Match(compDate,
                                                     ids,
                                                     setsScore=setsScore,
                                                     time='',
                                                     compName=compName + ', ' + compPlace))
#                        pointsScore = tokens[4].replace(', ', ',').replace(',', ';').replace(';0-0',
#                                                                                             '').replace(
#                            '-', ':').replace(':;', '').replace(';:', ''),

                                cm += 1
                                cmg += (1 - matches[-1].flError)
                                if matches[-1].flError == 0 and Match.checkSetsScore(matches[-1].setsScore):
                                    fout.write('\t'.join([str(e) for e in matches[-1].toArr()]) + '\t' + ';'.join(name1) + '\t' + ';'.join(name2) + '\n')
#                                    [[e.strip() for e in name1],
#                                     [e.strip() for e in name2]],
                                else:
                                    fout_err.write(line0.replace('\t', ';')[:-1] + '\n')
                                    #print(line0.replace('\t', ';')[:-1])
                                    fout_err.write('\t'.join([str(ee) for ee in matches[-1].toArr()]) + '\n')
                                    #print(matches[-1].toArr())
                                    fout_err.write('1 ' + '\t'.join(fp.split('\\')[-5:]) + '\t' + ';'.join(tokens) + '\n')
                                    #print('1 ' + '\t'.join(fp.split('\\')[-5:]) + '\t' + ';'.join(tokens) + '\n')

                                if tokens[0].lower() == 'па-ра':
                                    cp += 1
                                    cpg += (1 - matches[-1].flError)
                            else:
                                fout_err.write('2 ' + ';'.join(tokens) + '\n')
                                #print('2 ' + ';'.join(tokens))
                        else:
                            fout_err.write('flName ' + line0 + '\n')
                            #print('flName ' + line0)

                    #                    else:
#                        fout.write('\t'.join(fp.split('\\')[-5:]) + '\t' + ';'.join(tokens) + '\n')
                print(['/'.join(fp.split('\\')[-5:]), cm, cmg, cp, cpg])
                fout_err.write('\t'.join([str(ee) for ee in ['/'.join(fp.split('\\')[-5:]), cm, cmg, cp, cpg]]) + '\n')
    #filename = 'tabula-2016-17.-1-i-tur-muzhchiny.-super.-1-gr.tsv'
    #filename = '/КЧР/2016-2017/men/tabula-23.12-2-tur.-muzhchiny.-premer.tsv'
    #filename = r'\КЧР\2015-2016\men\Премьер-лига\4 тур\tabula-m-kchr-premer.-4-tur.4.tsv'
    #with open(dir + filename, encoding='utf-8') as fin:
    fout.close()

    print('\nMULTIPLE')
    for k, v in sorted(multiple.items(), key=lambda x: -x[1]):
        print([k, v])
    print('\nUNKNOWN')
    for k, v in sorted(unknown.items(), key=lambda x: -x[1]):
        print([k, v])

if __name__ == "__main__":
    main()