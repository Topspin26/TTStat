from os import walk
import time
import datetime as datetime
import random
import re

def rep(line):
    line = line.replace('ё', 'е')
    line = line.replace('Михаэль Таубер', 'Майкл Таубер')
    line = line.replace('Матан Ман', 'Ман Матан')
    line = line.replace('Идан Огурцев', 'Идан Угорцев')
    line = line.replace('Мустафа Дениз', 'Дениз Мустафа')
    line = line.replace('Рон Даймонд', 'Рон Димант')
    line = line.replace('Виктория Серебренникова', 'Виктория Серебрянникова')
    line = line.replace('Ирина Моцык', 'Ирина Моцик')
    line = line.replace('Мария Виноградова', 'Мария Быкова')
    line = line.replace('Ольга Овчинникова', 'Ольга Коренькова')
    line = line.replace('Петра Ловаш', 'Петра Ловас')
    line = line.replace('Ольга Баранова', 'Ольга Воробьева')
    line = line.replace('Наталья Сычева', 'Наталия Сычева')    
    return line

def main():
    with open('data/master_tour/corrections.txt', 'w', encoding='utf-8') as fout:
        for f in walk('data/master_tour/results_2016_06_21'):
            for ff in f[2]:
                with open('data/master_tour/results_2016_06_21/' + ff, 'r', encoding='utf-8') as fin1,\
                     open('data/master_tour/results/' + ff, 'r', encoding='utf-8') as fin2:
                        for line1, line2 in zip(fin1, fin2):
                            if rep(line1) != rep(line2): 
#                                print(line1)
#                                print(line2)
                                fout.write(line2)
                                fout.write(line1)
                    
                                

if __name__ == "__main__":
    main()