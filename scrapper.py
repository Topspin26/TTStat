from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import random
import re


def initDriver(url):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver', port = 5938)
    driver.get(url)
    time.sleep(3 + random.random()) # Let the user actually see something!
    return driver

def main():

#    url = 'https://live.fonbet.com/?locale=ru'
#    url = 'https://live.bkfon-bet.com/?locale=ru'
    url = 'http://www.bkfon.ru/ru/live/' #31.03.2016
    driver = initDriver(url)
#    e = driver.find_element_by_class_name('trSegment')
    iframes = driver.find_elements_by_xpath("//iframe")
#    print(iframes)            
    driver.switch_to_frame(iframes[1])
#    output = driver.page_source
#    print(output)
        

    k = 0
    kError = -1
    cntError = 0
    while (1):
        k += 1
        print(k)
        if k % 1440 == 0:
            driver.quit()
            driver = initDriver(url)
            iframes = driver.find_elements_by_xpath("//iframe")
            driver.switch_to_frame(iframes[1])
            
        timeout = 60
        eventsData = []
        curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            lineTable = driver.find_element_by_id('lineTable')
            print('lineTable - ok')
            sout = lineTable.get_attribute('outerHTML')
            print(len(sout))
            indexesSegment = [[m.start(), m.end(), 0] for m in re.finditer('<tr [^>]* id=\"segment(.)*?</tr>', sout)]
            indexesEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr [^>]* id=\"event(.)*?</tr>', sout)]
            indexes = sorted(indexesSegment + indexesEvent, key=lambda x: x[0])
            print(indexes)

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
            print('-----------')
            '''
            trs = lineTable.find_elements_by_xpath('//tr')
            flLine = 0
            segmentId = ''
            for tr in trs:
                try:
                    s = tr.get_attribute('outerHTML')
                    if s.find('trSegment') != -1:
                        flLine = 0
                        if s.find('sport3088') != -1:
                            flLine = 1
                            segmentId = tr.get_attribute('id')
                    if flLine == 1:
#                        print(s)
                        if segmentId != '':
                            eventsData.append([segmentId, s])
                            timeout = 5
                except Exception as e:
                    flLine = 0
#                    print('error1')
#                    print(str(e))
#                    fout.write('error1\n')
            '''
        except Exception as e:
            eventsData.append(['error', 'error2\n' + str(e)])
            print('error2')
            print(str(e))
            if kError == k - 1:
                cntError += 1
            else:
                cntError = 1
            if cntError == 5:
                timeout = 600
                cntError = 0
            kError = k
            driver.quit()
            driver = initDriver(url)
        
        '''
        lastEventId = ''
        fout = ''
        for e in eventsData:
            if e[0] != lastEventId:
                lastEventId = e[0]
                if fout != '':
                    fout.close()
                fout = open(e[0] + '.txt', 'a', encoding='utf-8')
            fout.write(curTime + '\t' + e[1] + '\n')
        if fout != '':
            fout.close()
        '''
        time.sleep(timeout)
            
    return

if __name__ == "__main__":
    main()