from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime
import random
import re
import os
from subprocess import Popen
import psycopg2

from BKFonLiveParser import *
import json

import config as config

chrome_options = Options()
#chrome_options.add_extension('chromedriver_win32/extension_2_0_327.crx')
#chrome_options.add_extension('chromedriver_win32/extension_3_0_0.crx')

class ScrapperLive:
    def __init__(self, driver, url):
        self.kError = -1
        self.k = 0
        self.cntError = 0
        self.eqCnt = 0
        self.timeout = 60
        self.url = url
        self.driver = driver
        self.lastEventsData = []
        self.eventsData = []

    def scrapp(self):
        self.k += 1
        try:
            if self.eqCnt == 16:
                self.driver = initDriver(self.url, self.driver)
                self.eqCnt = 0

            self.timeout = 60
            self.curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.eventsData = []
            tt = None
            try:
                tt = self.driver.find_element_by_xpath('//span[@class="events__filter-icon icon _type_sport _icon_3088"]')
            except:
                pass
            if tt is None:
                print('try click')
                self.driver.find_element_by_xpath('//div[@class="events__filter _type_sport"]/*/span[@class="events__filter-text"]').click()
                print('click')
                try:
                    tt = self.driver.find_element_by_xpath('//span[@class="events__filter-icon icon _type_sport _icon_3088"]')
                    print('find tt')
                    tt.click()
                except:
                    tt = None
            if tt:
                #print(self.driver.find_element_by_xpath("//*").get_attribute("outerHTML"))
                #print(self.driver.find_element_by_xpath('//div[@class="account__container"]').get_attribute('outerHTML'))
                lineTable = self.driver.find_element_by_xpath('//div[@class="table__flex-container"]/table[@class="table"]')
                print('lineTable - ok')
                sout = lineTable.get_attribute('outerHTML')
                print(len(sout))
                indexesSegment = [[m.start(), m.end(), 0] for m in re.finditer('<tr class=\"table__row _type_segment(.)*?</tr>', sout)]
                indexesEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr class=\"table__row"(.)*?</tr>', sout)]
                indexesBlockedEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr class=\"table__row _state_blocked"(.)*?</tr>', sout)]
                indexes = sorted(indexesSegment + indexesEvent + indexesBlockedEvent, key=lambda x: x[0])
                #print(indexes)

                flLine = 0
                segmentId = ''
                for ind in indexes:
                    if ind[2] == 0:
                        flLine = 0
        #                    print(sout[ind[0]:ind[1]])
                        if sout[ind[0]:ind[1]].find('sport_3088') != -1:
                            flLine = 1
        #                        ss = re.findall('segment[0-9]*', sout[ind[0]:ind[1]])
                            s = sout[ind[0]:ind[1]].split('<span class="table__title-text"')[1]
                            segmentId = s.split('>')[1].split('<')[0]
                            print(segmentId)
                    if flLine == 1:
                        if segmentId != '':
                            self.eventsData.append([segmentId, sout[ind[0]:ind[1]]])
                            self.timeout = 5
        #            for e in eventsData:
        #                print(e)
                print(len(self.eventsData))
            else:
                self.driver.find_element_by_xpath('//div[@class="events__filter _type_sport _state_expanded"]/*/span[@class="events__filter-text"]').click()
                print('no table-tennis')

        except Exception as e:
            self.eventsData.append(['error', 'error2\n' + str(e)])
            print('error2')
            print(str(e))
            if self.kError == self.k - 1:
                self.cntError += 1
            else:
                self.cntError = 1
                self.timeout = 5
            if self.cntError == 5:
                self.timeout = 60
                self.cntError = 0
            self.kError = self.k
            try:
                self.driver = initDriver(self.url, self.driver)
            except:
                pass

        if ('\t'.join([e[1] for e in self.eventsData]) == '\t'.join([e[1] for e in self.lastEventsData])):
            self.eqCnt += 1
        else:
            self.eqCnt = 0
        self.lastEventsData = self.eventsData.copy()

def initDriver(url, driver):
    #p = Popen("reconnect.bat")
    #p.wait()
    #time.sleep(15)
    if (True):#driver is None:
        try:
            driver.quit()
        except:
            pass
        driver = webdriver.Chrome('chromedriver_win32/chromedriver', chrome_options=chrome_options)
#        driver.get('chrome-extension://gjknjjomckknofjidppipffbpoekiipm/popup.html')
#        element = driver.find_element_by_id('connect')
#        element.click()
        driver.get(url)
    else:
        try:
            driver.refresh()
        except:
            driver = webdriver.Chrome('chromedriver_win32/chromedriver', chrome_options=chrome_options)
            driver.get(url)
            
    time.sleep(5 + random.random()) # Let the user actually see something!
    #iframes = driver.find_elements_by_xpath("//iframe")
    #driver.switch_to_frame(iframes[1])
    return driver

def main():

    con = None
    driver = None
    try:

        url = 'https://www.fonbet.ru/#/live' #31.03.2016
        url1 = 'https://www.fonbet.ru/#/bets'

        driver = initDriver(url, driver)

        con = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(config.DB_NAME,
                                                                            config.DB_USER,
                                                                            config.DB_PASSWORD))
        cur = con.cursor()

        tg = 60 * 60
        scrapper = ScrapperLive(driver, url)
        parser = BKFonLiveParserNew(maxCnt=-1)
        while (1):
            print((scrapper.k, scrapper.eqCnt))
            scrapper.scrapp()

            try:
                lastEventId = ''
                fout = ''
                block = []
                for e in scrapper.eventsData:
                    block.append(e[1])
                    if e[0] != lastEventId:
                        lastEventId = e[0]
                        if fout != '':
                            fout.close()
                        if e[0] != 'error':
                            e[0] = e[0]
                        if not os.path.exists('data/' + scrapper.curTime[:10]):
                            os.mkdir('data/' + scrapper.curTime[:10])
                        fout = open('data/' + scrapper.curTime[:10] + '/' + e[0] + '.txt', 'a', encoding='utf-8')
                    fout.write(scrapper.curTime + '\t' + e[1] + '\n')
                if fout != '':
                    fout.close()
                for matchBet in parser.addLineBlock(scrapper.curTime, block):
                    print(matchBet)
                    try:
                        info = '\t'.join([';'.join(matchBet.names[0]), ';'.join(matchBet.names[1]), json.dumps(matchBet.eventsInfo, ensure_ascii=False)])
                        cur.execute("INSERT INTO fonbet_live (datetime,evendId,compname,info) VALUES('{}','{}','{}','{}')".format(scrapper.curTime, matchBet.eventId, matchBet.compName, info))
                    except psycopg2.DatabaseError as e:
                        print('Error %s' % e)
                con.commit()
            except Exception as ex:
                print('writing error')
                print(ex)
                try:
                    fout.close()
                except:
                    pass

            time.sleep(scrapper.timeout + 10)
            tg += scrapper.timeout
            '''
            if tg >= 60 * 60:
                try:
                    driver.get(url1)
                    time.sleep(5 + random.random())
                
                    curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    eventsData = []
                    driver.find_element_by_xpath('//div[@class="events__filter _type_sport"]/*/span[@class="events__filter-text"]').click()
                    tt = driver.find_element_by_xpath('//span[@class="events__filter-icon icon _type_sport _icon_3088"]')
                    if tt:
                        tt.click()
    
                        lineTable = driver.find_element_by_xpath('//section[@class="table__inner"]/table[@class="table"]')
                        print('lineTable - ok')
                        sout = lineTable.get_attribute('outerHTML')
                        print(len(sout))
                        indexesSegment = [[m.start(), m.end(), 0] for m in re.finditer('<tr class=\"table__row _type_segment(.)*?</tr>', sout)]
                        indexesEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr class=\"table__row"(.)*?</tr>', sout)]
                        indexes = sorted(indexesSegment + indexesEvent, key=lambda x: x[0])
    
                        flLine = 0
                        segmentId = ''
                        for ind in indexes:
                            if ind[2] == 0:
                                flLine = 0
                                if sout[ind[0]:ind[1]].find('sport_3088') != -1:
                                    flLine = 1
                                    segmentId = sout[ind[0]:ind[1]].split('<span class="table__title-text">')[1].split('<')[0]
                                    print(segmentId)
                            if flLine == 1:
                                if segmentId != '':
                                    eventsData.append([segmentId, sout[ind[0]:ind[1]]])
                        print(len(eventsData))
                except Exception as e:
                    eventsData.append(['error', 'error2\n' + str(e)])
                    print('error2')
                    print(str(e))
    
    
                try:
                    lastEventId = ''
                    fout = ''
                    for e in eventsData:
                        if e[0] != lastEventId:
                            lastEventId = e[0]
                            if fout != '':
                                fout.close()
                            if e[0] != 'error':
                                e[0] = 'data_bets/' + e[0]
                            fout = open(e[0] + '.txt', 'a', encoding='utf-8')
                        fout.write(curTime + '\t' + e[1] + '\n')
                    if fout != '':
                        fout.close()
                except Exception as e:
                    print(str(e))
                    try:
                        fout.close()
                    except:
                        pass
                    print('writing error')
    
                try:
                    driver.get(url)
                    time.sleep(5 + random.random())
                except:
                    pass
                tg = 0
            '''
    finally:
        if con:
            con.close()
        if driver:
            driver.quit()

    return

if __name__ == "__main__":
    main()