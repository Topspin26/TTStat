from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import re


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = 5938)
    driver.get(url)
    time.sleep(random.random()) # Let the user actually see something!
    return driver

def scrappTournament(curDate, url):
    lines = []
    try:
        with open('data/master_tour/results/' + curDate + '.txt', 'r', encoding = 'utf-8') as fin:
            for line in fin:
                tokens = line.split('\t')
                lines.append(tokens[4])
    except:
        pass

#    if len(lines) != 0:
#        return 2
    
    driver = initDriver(url)
    lines2 = []
    try:
        table = driver.find_element_by_xpath('//*[@class = "table striped table-100"]')
        if type(table) is list:
            table = table[0]
        trs = table.find_elements(By.TAG_NAME, "tr")
        k = 0 
        dt = ''
        lines1 = []
        for tr in trs:
            k += 1
            if k == 1:
                continue
            s = tr.get_attribute('outerHTML')
            if s.find('sheduleTableSeparator') != -1:
                sdt = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute('innerHTML')
                dt = datetime.datetime.strptime(sdt, "%d.%m.%Y").date().strftime("%Y-%m-%d")
                print(dt)
            else:
                tds = tr.find_elements(By.TAG_NAME, "td")
                tt = tds[0].get_attribute('innerHTML')
                p1 = tds[2].find_elements(By.TAG_NAME, "a")[0].get_attribute('innerHTML')
                p2 = tds[3].find_elements(By.TAG_NAME, "a")[0].get_attribute('innerHTML')
                sets_score = tds[4].get_attribute('innerHTML')
                match_score = tds[5].get_attribute('innerHTML')
                lines1.append(dt + '\t' + tt + '\t' + p1 + '\t' + p2 + '\t' + sets_score + '\t' + match_score + '\n')
                lines2.append(sets_score)
                print(dt + ' ' + tt + '\t' + p1 + '\t' + p2 + '\t' + sets_score + '\t' + match_score)
    except:
        pass
    driver.close()
    
    fl = 0
    if len(lines) != len(lines2):
        fl = 1
    else:
        for i,e in enumerate(lines):
            if e.strip() != lines2[i].strip():
                fl = 1
                break

    if fl == 1:
        with open('data/master_tour/results/' + curDate + '.txt', 'w', encoding = 'utf-8') as fout:
            for line in lines1:
                fout.write(line)

    return fl
                
def main():

#    fl = scrappTournament('2013-01-01', 'http://master-tour.pro/tournaments/2013-01-01.html')
#    return

    url = 'http://master-tour.pro/archive-new.html'

    driver = initDriver(url)

    curDate = '2016-05-18'
    
    lastUrl = ''
    while (1):
        try:
#            href = driver.find_element_by_xpath('//*[@href="/tournaments/' + curDate + '.html"]')
#            print(href.get_attribute('outerHTML'))
#            tUrl = href.get_attribute('outerHTML').split('"')[1]
            tUrl = 'http://master-tour.pro/tournaments/' + curDate + '.html'
            print(tUrl + '\t', end = '')
#            if lastUrl != tUrl:
#                scrappTournament(curDate, 'http://master-tour.pro' + tUrl)
#                lastUrl = tUrl
            fl = scrappTournament(curDate, tUrl)
            print(fl)
        except:
            pass
        if curDate == datetime.datetime.now().strftime("%Y-%m-%d"):
            break
        curDate = (datetime.datetime.strptime(curDate, "%Y-%m-%d").date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
#        print(curDate)
        continue
    
    driver.quit()        
    return

if __name__ == "__main__":
    main()