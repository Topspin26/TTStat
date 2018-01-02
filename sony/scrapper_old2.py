from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime
import random
import re
import os
from subprocess import Popen

chrome_options = Options()
#chrome_options.add_extension('chromedriver_win32/extension_2_0_327.crx')
#chrome_options.add_extension('chromedriver_win32/extension_3_0_0.crx')

def initDriver(url, driver):
    p = Popen("reconnect.bat")
    p.wait()
    time.sleep(15)
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
            
    time.sleep(10 + random.random()) # Let the user actually see something!
    #iframes = driver.find_elements_by_xpath("//iframe")
    #driver.switch_to_frame(iframes[1])
    return driver

def main():


    url = 'https://www.bkfon.ru/live/#3088' #31.03.2016
    url1 = 'https://www.bkfon.ru/bets/#3088'

#    url = 'https://live.fonbet.com/?locale=ru'
#    url = 'https://live.bkfon-bet.com/?locale=ru'
#    url = 'http://www.bkfon.ru/ru/live/' #31.03.2016
#    url = 'https://live.bet-in-fon.com/?locale=ru' #25.06.2016
    driver = None
    driver = initDriver(url, driver)
    #driver = initDriver(url, driver)
#    e = driver.find_element_by_class_name('trSegment')
#    print(iframes)            
#    output = driver.page_source
#    print(output)
    
    k = 0
    kError = -1
    cntError = 0
    lastEventsData = []
    eventsData = []
    eqCnt = 0
    tg = 60 * 60
    while (1):
        k += 1
        print((k, eqCnt))
        try:
            if eqCnt == 30:
                #driver.quit()
                driver = initDriver(url, driver)
                eqCnt = 0
                
            timeout = 60
            eventsData = []
            curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            lineTable = driver.find_element_by_id('lineTable')
            print('lineTable - ok')
            sout = lineTable.get_attribute('outerHTML')
            print(len(sout))
            indexesSegment = [[m.start(), m.end(), 0] for m in re.finditer('<tr [^>]* id=\"segment(.)*?</tr>', sout)]
            indexesEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr [^>]* id=\"event(.)*?</tr>', sout)]
            indexes = sorted(indexesSegment + indexesEvent, key=lambda x: x[0])
#            print(indexes)

            flLine = 0
            segmentId = ''
            for ind in indexes:
                if ind[2] == 0:
                    flLine = 0
                    if sout[ind[0]:ind[1]].find('sport3088') != -1:
                        flLine = 1
                        ss = re.findall('segment[0-9]*', sout[ind[0]:ind[1]])
                        segmentId = ss[0]
#                        print(segmentId)
                if flLine == 1:
                    if segmentId != '':
                        eventsData.append([segmentId, sout[ind[0]:ind[1]]])
                        timeout = 5
#            for e in eventsData:
#                print(e)
            print(len(eventsData))
                
        except Exception as e:
            eventsData.append(['error', 'error2\n' + str(e)])
            print('error2')
            print(str(e))
            if kError == k - 1:
                cntError += 1
            else:
                cntError = 1
                timeout = 5
            if cntError == 5:
                timeout = 60
                cntError = 0
            kError = k
            try:
                #driver.quit()
                driver = initDriver(url, driver)
            except Exception as e:
                foo = 0
        
        try:
            lastEventId = ''
            fout = ''
            for e in eventsData:
                if e[0] != lastEventId:
                    lastEventId = e[0]
                    if fout != '':
                        fout.close()
                    if e[0] != 'error':
                        e[0] = e[0]
                    if not os.path.exists('data/' + curTime[:10]):
                        os.mkdir('data/' + curTime[:10])
                    fout = open('data/' + curTime[:10] + '/' + e[0] + '.txt', 'a', encoding='utf-8')
                fout.write(curTime + '\t' + e[1] + '\n')
            if fout != '':
                fout.close()
        except:
            try:
                fout.close()
            except:
                foo = 0
            print('writing error')
        
        if ('\t'.join([e[1] for e in eventsData]) == '\t'.join([e[1] for e in lastEventsData])):
            eqCnt += 1
        else:
            eqCnt = 0
        lastEventsData = eventsData.copy()
        time.sleep(timeout)
        tg += timeout
        if tg >= 60 * 60:
            try:
                driver.get(url1)
                time.sleep(15 + random.random())
            
                curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                eventsData = []
                
                lineTable = driver.find_element_by_id('lineTable')
                print('lineTable - ok')
                sout = lineTable.get_attribute('outerHTML')
                print(len(sout))
                indexesSegment = [[m.start(), m.end(), 0] for m in re.finditer('<tr [^>]* id=\"segment(.)*?</tr>', sout)]
                indexesEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr [^>]* id=\"event(.)*?</tr>', sout)]
                indexes = sorted(indexesSegment + indexesEvent, key=lambda x: x[0])
            
                flLine = 0
                segmentId = ''
                for ind in indexes:
                    if ind[2] == 0:
                        flLine = 0
                        if sout[ind[0]:ind[1]].find('sport3088') != -1:
                            flLine = 1
                            ss = re.findall('segment[0-9]*', sout[ind[0]:ind[1]])
                            segmentId = ss[0]
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
                    foo = 0
                print('writing error')

            try:
                driver.get(url)
                time.sleep(5 + random.random())
            except:
                pass
            tg = 0
            
    return

if __name__ == "__main__":
    main()