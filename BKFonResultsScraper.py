from datetime import datetime
import random
from common import *
from Logger import Logger


def getResults(curDate):
    s = None
    try:
        with open('data/bkfon/results/' + curDate + '_new.txt', 'r', encoding='utf-8') as fin:
            s = next(fin)
    except:
        s = None
    return s


class BKFonResultsScraper:
    @staticmethod
    def run(logger=Logger()):
        print('BKFonResultsScraper')
        logger.print('BKFonResultsScraper')
        url = 'https://www.fonbet.ru/#!/results'
        driver = initDriver(url, 10)
        try:
            monthname2Num = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'май': 5, 'мая': 5, 'июн': 6, 'июл': 7, 'авг': 8,
                             'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12}

            tDate = datetime.now().strftime("%Y-%m-%d")

            flLast = 1
            flExit = 0
            while flExit == 0:
                if flLast == 1:
                    driver.find_element_by_xpath('//span[@class="events__filter-down icon _icon_arrow-tree-light"]').click()
                s = driver.find_element_by_class_name('ui-calendar__title').get_attribute('innerHTML')
                month = monthname2Num[s.lower()[:3]]
                logger.print(month)
                year = s.lower()[-4:]
                logger.print(year)

                active_days = driver.find_elements_by_xpath(
                    '//td[contains(@class, "ui-calendar__col") and not (contains(@class, "_state_off"))]/a')
                nd = len(active_days)
                logger.print(len(active_days))
                if year == str(datetime.now().year):
                    for i in range(nd - flLast):
                        #if month == 4:
                        #    continue
                        #if i < 7:
                        #    continue
                        if month != datetime.now().month and (datetime.now().day > 14 or month != datetime.now().month - 1):
                            flExit = 1
                            continue
                        curDate = year + '-' + str(month).zfill(2) + '-' + str(i + 1).zfill(2)
                        logger.print(curDate)
                        filename = 'data/bkfon/results/' + curDate + '_new.txt'
                        sLast = getResults(curDate)

                        logger.print(active_days[i].get_attribute('innerHTML'))
                        active_days[i].click()
                        time.sleep(10 + random.random())

                        tt = None
                        try:
                            tt = driver.find_element_by_xpath(
                                '//span[@class="events__filter-icon icon _type_sport _icon_13"]')
                        except:
                            pass
                        if tt is None:
                            logger.print('try click')
                            try:
                                driver.find_element_by_xpath(
                                    '//div[@class="events__filter _type_sport"]/*/span[@class="events__filter-text"]').click()
                            except:
                                time.sleep(2)
                                driver.find_element_by_xpath(
                                    '//div[@class="events__filter _type_sport"]/*/span[@class="events__filter-text"]').click()
                            logger.print('click')
                            try:
                                tt = driver.find_element_by_xpath(
                                    '//span[@class="events__filter-icon icon _type_sport _icon_3088"]')
                                logger.print('find tt')
                                tt.click()
                            except:
                                tt = None

                        if tt:
                            s = driver.find_element_by_xpath('//div[@class="results_table"]').get_attribute('innerHTML')
                            if sLast is None:
                                with open(filename, 'w', encoding='utf-8') as fout:
                                    fout.write(s)
                            elif sLast.strip() != s.strip():
                                arr1 = s.split('class="table__row')
                                arr2 = sLast.split('class="table__row')
                                flNewInfo = 0
                                for e in arr2:
                                    if not (e in arr1):
                                        flNewInfo = 1
                                        logger.print(e)
                                if flNewInfo == 1:
                                    logger.print(curDate + ' NEW INFO')
                                    with open(filename, 'w', encoding='utf-8') as fout:
                                        fout.write(s)
                                    with open(filename[:-4] + '_old' + tDate + '.txt', 'w', encoding='utf-8') as fout:
                                        fout.write(sLast)
                        else:
                            driver.find_element_by_xpath(
                                '//div[@class="events__filter _type_sport"]/*/span[@class="events__filter-text"]').click()
                            logger.print('no table-tennis')

                        driver.find_element_by_xpath(
                            '//span[@class="events__filter-down icon _icon_arrow-tree-light"]').click()
                        active_days = driver.find_elements_by_xpath(
                            '//td[contains(@class, "ui-calendar__col") and not (contains(@class, "_state_off"))]/a')
    #                   return
                else:
                    flExit = 1
                    break
                driver.find_element_by_xpath('//a[@class="ui-calendar__nav _pos_left"]').click()
                time.sleep(10 + random.random())
                flLast = 0
                continue
        finally:
            if driver:
                driver.quit()


def main():
    BKFonResultsScraper.run(logger=Logger('BKFonResultsScraper.txt'))


if __name__ == "__main__":
    main()
