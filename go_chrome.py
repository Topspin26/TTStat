from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

def initDriver(url):
    driver = webdriver.Chrome('D:/Programming/Python/chromedriver_win32/chromedriver')
    driver.get(url)
    time.sleep(3 + random.random()) # Let the user actually see something!
    return driver

def main():

    url = 'http://ya.ru'
    driver = initDriver(url)
    driver.quit()
#    e = driver.find_element_by_class_name('trSegment')
    '''
    k = 0
    kError = -1
    cntError = 0
    while (1):
        k += 1
        print(k)
        if k % 200 == 0:
            driver.quit()
            driver = initDriver(url)            
        timeout = 60
        eventsData = []
        try:
            lineTable = driver.find_element_by_id('lineTable')
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
        except Exception as e:
            eventsData.append(['error', 'error2\n' + str(e)])
            print('error2')
            print(str(e))
            if kError == k - 1:
                cntError += 1
            else:
                cntError = 1
            if cntError == 5:
                break
            kError = k
            driver.quit()
            driver = initDriver(url)
        
        lastEventId = ''
        fout = ''
        for e in eventsData:
            if e[0] != lastEventId:
                lastEventId = e[0]
                if fout != '':
                    fout.close()
                fout = open(e[0] + '.txt', 'a', encoding='utf-8')
            fout.write(e[1] + '\n')
        if fout != '':
            fout.close()
        
        time.sleep(timeout)
    '''        
    return

if __name__ == "__main__":
    main()