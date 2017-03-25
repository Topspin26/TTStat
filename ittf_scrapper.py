from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime as datetime
import random
import re
import os
from os import walk


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = 5938)
    driver.get(url)
    #time.sleep(2) # Let the user actually see something!
    return driver

'''
def readIttfPlayers():
    playersDict = dict()
    with open('data/ittf/ittf_players.txt', 'r', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            tokens = [e.strip() for e in tokens]
            playersDict[tokens[1]] = tokens[0]
    return playersDict
'''
def getIttfMatches(driver, url, pages):
#    playersDict = readIttfPlayers()

    unchanged = 0

    for page in pages:
        print([page, unchanged])
        flPage = 0
        if unchanged == 20:
            break
        driver.get(url + str(page))

        tds = driver.find_elements_by_xpath('//*//table[@bordercolor = "#000080"]//tr//td')
        playerId = None
        playerRating = None
        numCols = 6
        matches = dict()
        match = []
        for i,td in enumerate(tds[:-1]):
            tokens = td.get_attribute('innerHTML').replace('\t', '').replace('\n', '').split('<br>')
            if i % numCols == 1 or i % numCols == 3:
                tokensNew = []
                for e in tokens:
                    if len(re.sub('<[^<]+?>', '', e).strip()) > 0:
                        tokensNew.append(e)
                        result = re.search('P_ID=([^&]*)&', e)
                        tokensNew.append(result.group(1))
                tokens = tokensNew
            tokens = [re.sub('<[^<]+?>', '', e).strip() for e in tokens]
            match.append(tokens)
            if i % numCols == 5:
#                print(match)
                dt = match[0][-1]
                try:
                    arr = dt.split(' ')[-1].split('/')
                    dt = arr[2] + '-' + arr[1].zfill(2) + '-' + arr[0].zfill(2)
                except:
                    dt = 'error_' + dt.replace('/', '_').replace('\\', '_')
                if not dt in matches:
                    matches[dt] = []
                matches[dt].append([';'.join(e) for e in match])
                match = []
        for e in matches.items():
            try:
                rows = []
                flChange = 0
                if os.path.exists('data/ittf/results/' + e[0] + '.txt'):
                    with open('data/ittf/results/' + e[0] + '.txt', encoding = 'utf-8') as fin:
                        for line in fin:
                            rows.append(line.strip().split('\t'))
                    for s in e[1]:
                        fl = 0
                        for ir,row in enumerate(rows):
                            if row[0] == s[0] and row[1] == s[1] and row[3] == s[3]:
                                if '\t'.join(row) != '\t'.join(s):
                                    print('CHANGE')
                                    print(row)
                                    print(s)
                                    rows[ir] = s
                                    flChange = 1
                                fl = 1
                                break
                        if fl == 0:
                            print('NEW')
                            print(s)
                            flChange = 1
                            rows.append(s)
                else:
                    flChange = 1
                    rows = e[1]
                if flChange == 1:
                    flPage = 1
                    with open('data/ittf/results/' + e[0] + '.txt', 'w', encoding='utf-8') as fout:
                        for s in rows:
                            fout.write('\t'.join(s) + '\n')
            except Exception as ex:
                print(str(ex))
        if flPage == 1:
            unchanged = 0
        else:
            unchanged += 1

def main():

    url = 'http://www.old.ittf.com/competitions/matches_per_player_all.asp?P_ID=&Formrnd64_Page='
    driver = initDriver(url)
    getIttfMatches(driver, url, list(range(1,101)))


if __name__ == "__main__":
    main()