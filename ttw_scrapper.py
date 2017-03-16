from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import os
import re
from os import walk


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver')#, port = 5938)
    driver.get(url)
    time.sleep(1 + random.random()) # Let the user actually see something!
    return driver

def scrappPage(url, playersInfo):
    driver = initDriver(url)
    table = driver.find_element_by_xpath('//*[@class = "player-list"]')
    trs = table.find_elements(By.TAG_NAME, "tr")
    sh = []
    for tr in trs[1:]:
        hr = tr.find_elements(By.TAG_NAME, "a")[0]
        games = tr.find_elements(By.TAG_NAME, "td")[4].get_attribute('innerHTML').split(',')[0]
        s = hr.get_attribute('innerHTML')
        href = hr.get_attribute('href')
        #print([s, href, games])
        sh.append([s, href, games])
        #        break

    cc = 0
    for s, href, games in sh:
        cc += 1
        plId = href.split('=')[-1]
        plName = s
        print([s, href, games])
        if not (plId in playersInfo) or playersInfo[plId][1] != games:
            name1 = plName + ';' + plId
            driver.get(href)
            table = driver.find_elements_by_xpath('//*[@class = "player-list"]')[1]
            trs = table.find_elements(By.TAG_NAME, "tr")
            rows = []
            compId = None
            compName = None
            dt = None
            lines = None
            fout = None
            for tr in trs:
                # print(tr.get_attribute('innerHTML').strip())
                tds = tr.find_elements(By.TAG_NAME, "td")
                if len(tds) == 0:
                    th = tr.find_elements(By.TAG_NAME, "th")[0]
                    if th.get_attribute('class') == "cell-lefted":
                        hr = th.find_elements(By.TAG_NAME, "a")[0]
                        s = hr.get_attribute('innerHTML')
                        href = hr.get_attribute('href')
                        compName = s[:-12].strip().replace('"', '').replace('/', ' ').replace('\\', ' ')
                        dt = s[-5:-1] + '-' + s[-8:-6] + '-' + s[-11:-9]
                        compId = href.split('=')[-1]
                        print([compName, dt, compId, href])
                        if dt >= '2014':
                            dirname = 'data/ttw/results/' + dt
                            if not os.path.exists(dirname):
                                os.mkdir(dirname)
                            filename = compId + '_' + compName + '.txt'
                            lines = set()
                            if os.path.exists(dirname + '/' + filename):
                                with open(dirname + '/' + filename, encoding='utf-8') as fin:
                                    for line in fin:
                                        lines.add(line.strip())
                            if fout:
                                fout.close()
                            fout = open(dirname + '/' + filename, 'a', encoding='utf-8')
                        else:
                            break
                else:
                    if dt >= '2014':
                        name2 = ''
                        score = ''
                        for i, td in enumerate(tds):
                            if i == 0:
                                score = td.get_attribute('innerHTML').replace(':', '-')
                            elif i == 1:
                                name2 = td.find_elements(By.TAG_NAME, "a")[0].get_attribute('innerHTML')
                                name2 += ';' + td.find_elements(By.TAG_NAME, "a")[0].get_attribute('href').split('=')[-1]
                        # print([dt, compName, name1, name2, score])
                        row = '\t'.join([dt, compName, name1, name2, score])
                        if not (row in lines):
                            fout.write(row + '\n')
            if fout:
                fout.close()
            playersInfo[plId] = [plName, games]
            if cc % 10 == 0:
                with open('data/ttw/players_info.txt', 'w', encoding='utf-8') as fout:
                    for k,v in sorted(playersInfo.items(), key = lambda x: x[0]):
                        fout.write(k + '\t' + v[0] + '\t' + v[1] + '\n')
    with open('data/ttw/players_info.txt', 'w', encoding='utf-8') as fout:
        for k, v in sorted(playersInfo.items(), key=lambda x: x[0]):
            fout.write(k + '\t' + v[0] + '\t' + v[1] + '\n')
    driver.quit()

def main():
    playersInfo = dict()
    with open('data/ttw/players_info.txt', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.rstrip().split('\t')
            playersInfo[tokens[0]] = tokens[1:]
    for e in range(0, 1001, 500):
        url = 'http://ttw.ru/ttw-rs/index.php?litera=rating&page=' + str(e)
        scrappPage(url, playersInfo)

if __name__ == "__main__":
    main()