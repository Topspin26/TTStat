from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import random
import os
import re
from subprocess import Popen


def initDriver(url, driver):
    driver = webdriver.Chrome('chromedriver_win32/chromedriver')#, port = 5938)
    driver.get(url)
    time.sleep(1 + random.random()) # Let the user actually see something!
    return driver

def getResults(curDate):
    s = None
    try:
        with open('data/bkfon/results/' + curDate + '.txt', 'r', encoding = 'utf-8') as fin:
            s = next(fin)
    except:
        s = None
    return s

def main():
    url = 'https://www.bkfon.ru/results'
    driver = None
    driver = initDriver(url, driver)

    monthname2Num = {'янв':1,'фев':2,'мар':3,'апр':4,'май':5,'июн':6,'июл':7,'авг':8,'сен':9,'окт':10,'ноя':11,'дек':12}

    tDate = datetime.now().strftime("%Y-%m-%d")

    flLast = 1
    flExit = 0
    while (flExit == 0):
        month = driver.find_element_by_class_name('ui-datepicker-month').get_attribute('innerHTML')
        month = monthname2Num[month.lower()[:3]]
        print(month)
        year = driver.find_element_by_class_name('ui-datepicker-year').get_attribute('innerHTML')
        print(year)
        active_days = driver.find_elements(By.XPATH, "//*[@data-handler='selectDay']")
        nd = len(active_days)
        print(len(active_days))
        if year == '2017':
            for i in range(nd - flLast):
                if month != 2 and month != 3:
                    continue
                curDate = year + '-' + str(month).zfill(2) + '-' + str(i + 1).zfill(2)
                print(curDate)
                filename ='data/bkfon/results/' + curDate + '.txt'
                sLast = getResults(curDate)

                print(active_days[i].get_attribute('innerHTML'))
                active_days[i].click()
                time.sleep(5 + random.random())
                active_days = driver.find_elements(By.XPATH, "//*[@data-handler='selectDay']")
                s = driver.find_element_by_id('resultDiv').get_attribute('innerHTML')
                if sLast is None:
                    with open(filename, 'w', encoding = 'utf-8') as fout:
                        fout.write(s)
                elif sLast.strip() != s.strip():
                    arr1 = s.split('class="resultTd"')
                    arr2 = sLast.split('class="resultTd"')
                    flNewInfo = 0
                    for e in arr2:
                        if not (e in arr1):
                            flNewInfo = 1
                            print(e)
                    if flNewInfo == 1:
                        print(curDate + ' NEW INFO')
                        with open(filename, 'w', encoding='utf-8') as fout:
                            fout.write(s)
                        with open(filename[:-4] + '_old' + tDate + '.txt', 'w', encoding='utf-8') as fout:
                            fout.write(sLast)
        #                    return
        else:
            flExit = 1
            break
        driver.find_element_by_class_name('ui-datepicker-prev').click()
        time.sleep(5 + random.random())
        flLast = 0
        continue
    return


if __name__ == "__main__":
    main()