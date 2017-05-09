from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import os
from common import *

def scrappMonth(month):
    url = 'http://or.rttf.ru/tournaments/' + month
    driver = initDriver(url)
    table = driver.find_element_by_xpath('//*[@class = "tournaments"]')
    hrs = table.find_elements(By.TAG_NAME, "a")
    sh = []
    for hr in hrs:
        s = hr.get_attribute('innerHTML')
        href = hr.get_attribute('href')
        sh.append([s, href])
    for s, href in sh:
        dt = s[6:10] + '-' + s[3:5] + '-' + s[:2]
        dirname = 'data/rttf/results/' + dt
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        print([s, href])
        compId = href.split('/')[-1]
        compName = s.split(' ', 1)[-1].replace('"', '')
        filenameMatches = compId + '_' + compName + '.txt'
        filenameRankings = compId + '_' + compName + '_rankings.txt'
        if os.path.exists(dirname + '/' + filenameMatches) and os.path.exists(dirname + '/' + filenameRankings):
            continue
        driver.get(href)

        if not os.path.exists(dirname + '/' + filenameMatches):
            print('matches')
            table = driver.find_element_by_xpath('//*[@class = "games"]')
            trs = table.find_elements(By.TAG_NAME, "tr")
            rows = []
            for tr in trs:
                tds = tr.find_elements(By.TAG_NAME, "td")
                name1 = name2 = ''
                score = ''
                for i, td in enumerate(tds):
                    if i == 0:
                        name1 = td.find_element(By.TAG_NAME, "a").get_attribute('innerHTML').strip()
                        name1 += ';' + td.find_element(By.TAG_NAME, "a").get_attribute('href').split('/')[-1]
                    elif i == 1 or i == 3:
                        score += td.get_attribute('innerHTML').replace('&nbsp;', '').strip()
                    elif i == 2:
                        score += '-'
                    else:
                        name2 = td.find_element(By.TAG_NAME, "a").get_attribute('innerHTML').strip()
                        name2 += ';' + td.find_element(By.TAG_NAME, "a").get_attribute('href').split('/')[-1]
                # print([name1, name2, score])
                rows.append([dt, compName, name1, name2, score])
            with open(dirname + '/' + filenameMatches, 'w', encoding='utf-8') as fout:
                for row in rows:
                    fout.write('\t'.join(row) + '\n')

        if not os.path.exists(dirname + '/' + filenameRankings):
            print('rankings')
            table = driver.find_element_by_xpath('//*[@class = "players"]')
            trs = table.find_elements(By.TAG_NAME, "tr")
            rows = []
            for tr in trs[1:]:
                tds = tr.find_elements(By.TAG_NAME, "td")
                name = tds[1].find_element(By.TAG_NAME, "a").get_attribute('innerHTML').strip()
                name += ';' + tds[1].find_element(By.TAG_NAME, "a").get_attribute('href').split('/')[-1]
                rank = tds[3].get_attribute('innerHTML').strip()
                drank = tds[4].get_attribute('innerHTML').strip()
                #print(name, rank, drank)
                rows.append([dt, compName, name, rank, drank])
            with open(dirname + '/' + filenameRankings, 'w', encoding='utf-8') as fout:
                for row in rows:
                    fout.write('\t'.join(row) + '\n')

    driver.quit()


def main():
    for year in range(2017, 2018):
        for month in range(1, 13):
            scrappMonth(str(year) + '-' + str(month).zfill(2))
            if year == 2017 and month == 5:
                break

if __name__ == "__main__":
    main()