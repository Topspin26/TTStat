from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import os
import datetime
from common import *

def scrappTournament(url, id, dts):
    startDate = dts[-4:] + '-' + dts[3:5] + '-' + dts[:2]
    filename = 'data/challenger_series/results/' + startDate + '_' + id + '.txt'
#    if os.path.exists(filename):
#        return

    driver = initDriver(url)
    table = driver.find_element_by_xpath('//*[@class = "rounds"]')
    trs = table.find_elements(By.TAG_NAME, "tr")
    days = {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}
    fl = -1
    rows = []
    for tr in trs[2:-1]:
        tds = tr.find_elements(By.TAG_NAME, "td")
        if tds[0].get_attribute('innerHTML').replace('<strong>', '').replace('</strong>', '') in days:
            fl += 1
        t = tds[1].get_attribute('innerHTML')
        score = tds[3].get_attribute('innerHTML').replace(':', '-')
        t = t.replace('18:300', '18:30').replace('28:40', '18:40')
        if t.lower() == 'cancel' or score.lower() == 'cancel' or t.lower() == 'injure':
            continue
        name1 = tds[4].get_attribute('innerHTML').replace(',', '').replace('<strong>', '').replace('</strong>', '')
        name2 = tds[5].get_attribute('innerHTML').replace(',', '').replace('<strong>', '').replace('</strong>', '')
        tt = ''
        mdt = ''
        if t != '-':
            curDate = (datetime.datetime.strptime(startDate + ' ' + t, "%Y-%m-%d %H:%M") + datetime.timedelta(days=fl) + datetime.timedelta(hours=2))
            mdt = curDate.strftime("%Y-%m-%d")
            tt = curDate.strftime("%H:%M")
        else:
            mdt = (datetime.datetime.strptime(startDate, "%Y-%m-%d") + datetime.timedelta(days=fl)).strftime("%Y-%m-%d")
        rows.append('\t'.join([mdt, tt, name1, name2, score]))
        print(rows[-1])

    with open(filename, 'w', encoding='utf-8') as fout:
        for row in rows:
            fout.write(row + '\n')
    driver.quit()


def main():
    url = 'http://challengerseries.net/content/results'

    driver = initDriver(url)
    arr = driver.find_element_by_xpath('//*[@id = "headselect"]').find_elements(By.TAG_NAME, "option")
    ids = []
    for e in arr:
        print([e.get_attribute('value'), e.get_attribute('innerHTML')])
        ids.append([e.get_attribute('value'), e.get_attribute('innerHTML')])
    driver.quit()

    ids.reverse()

    j = 0
    for id,dt in ids:
        startDate = dt[-4:] + '-' + dt[3:5] + '-' + dt[:2]
        filename = 'data/challenger_series/results/' + startDate + '_' + id + '.txt'
        if not os.path.exists(filename):
            break
        j += 1
    j = max(j - 2, 0)

    print(len(ids), j)

    #ids = [['1035', '27.02. - 28.02.2017']]
    for id,dt in ids[j:]:
        print([id, dt])
#        if id == '1040':
#            break
        scrappTournament(url + '?q=node/' + id, id, dt)
        #break

if __name__ == "__main__":
    main()