from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import os
from os import walk
from common import *

def scrapp(tid):
    url = 'http://tt-liga.pro/tours/' + str(tid)
    driver = initDriver(url)
    if driver.current_url.find('404.php') != -1:
        driver.quit()
        return 1
    compName = driver.find_element_by_tag_name('h1').get_attribute('innerHTML')
    dt = driver.find_elements_by_xpath('//*[@class = "day"]')[0].get_attribute('innerHTML')
    st = driver.find_elements_by_xpath('//*[@class = "day"]')[1].get_attribute('innerHTML')
    place = driver.find_elements_by_xpath('//div[@class = "desc"]/div[@class = "desc-item"]/a')[0].get_attribute('text')
    monthname2Num = {'Янв':1,'Фев':2,'Мар':3,'Апр':4,'Май':5,'Мая':5,'Июн':6,'Июл':7,'Авг':8,'Сен':9,'Окт':10,'Ноя':11,'Дек':12}
    dt = dt.split(' ')[2] + '-' + str(monthname2Num[dt.split(' ')[1]]).zfill(2) + '-' + dt.split(' ')[0].zfill(2)
    compInfo = compName + ';' + place + ';' + st
    print([dt, compInfo])
    lines2 = []
    trs = driver.find_elements_by_xpath('//div[@class="item"]//table[@class="games_list"]/tbody/tr')
    for tr in trs[1:]:
        tds = tr.find_elements_by_xpath('.//td[@class="center"]')
        if len(tds) == 1:
            stage = tds[0].get_attribute('innerHTML').replace('<b>', '').replace('</b>', '').strip()
            print(stage)
        else:
            print()
            s = tr.find_element_by_xpath('./td').get_attribute('innerHTML')
            tt = s.split('>')[1][:5]

            s = tr.find_element_by_xpath('./td[@class = "right"]').get_attribute('innerHTML')
            pl1Id = s.split('">')[0].split('/')[1]
            pl1Name = s.split('">')[1].split('<')[0]

            s = tr.find_element_by_xpath('./td[@class = "left"]').get_attribute('innerHTML')
            pl2Id = s.split('">')[0].split('/')[1]
            pl2Name = s.split('">')[1].split('<')[0]

            r1 = tr.find_elements_by_xpath('./td[@class = "rating"]/b')[0].get_attribute('innerHTML')
            r2 = tr.find_elements_by_xpath('./td[@class = "rating"]/b')[1].get_attribute('innerHTML')
            try:
                dr1 = tr.find_elements_by_xpath('./td[@class = "rating"]/small')[0].get_attribute('innerHTML')
                dr2 = tr.find_elements_by_xpath('./td[@class = "rating"]/small')[1].get_attribute('innerHTML')
            except:
                dr1 = '0'
                dr2 = '0'
                print('wrong dr')

            try:
                score = tr.find_elements_by_xpath('./td[@class = "score"]/table/tbody/tr/td')[1].get_attribute('innerHTML')
                gameId = score.split('">')[0].split('/')[1]
                score = score.split('>')[1].split('<')[0]
                pointsScore = tr.find_element_by_xpath('./td[@class = "score"]/small').get_attribute('innerHTML')
            except:
                score = ''
                gameId = ''
                pointsScore = ''
                print('wrong score')

            lines2.append('\t'.join([dt, tt, compInfo, gameId, stage, pl1Name + ';' + pl1Id, r1, dr1, pl2Name + ';' + pl2Id, r2, dr2, score, pointsScore]))
            print([dt, tt, compInfo, gameId, stage, pl1Name + ';' + pl1Id, r1, dr1, pl2Name + ';' + pl2Id, r2, dr2, score, pointsScore])

    driver.quit()

    filename = 'data/liga_pro/results/' + dt + '_' + str(tid) + '_' + compName + '.txt'
    with open(filename, 'w', encoding = 'utf-8') as fout:
        for line in lines2:
            fout.write(line + '\n')
    return 0

def main():
    curId = 1
    for f in walk('data/liga_pro/results'):
        for ff in f[2]:
            curId = max(curId, int(ff.split('_')[1]))
    curId = max(1, curId - 2)
    print(curId)
    fl = 0
    for tid in range(curId, 300):
        print(tid)
        fl += scrapp(tid)
        if fl == 2:
            break

if __name__ == "__main__":
    main()