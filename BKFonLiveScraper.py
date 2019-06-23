import time
from datetime import datetime
import random
import re
import os
from subprocess import Popen
import psycopg2
import json

from BKFonLiveParser import *
from driver import Driver


class SportName:
    names = {'3088': 'Настольный теннис'}


class BKFonLiveScraper:

    @staticmethod
    def parse(sout, sport='3088'):
        events_data = []

        indexesSegment = [[m.start(), m.end(), 0] for m in
                          re.finditer('<tr class=\"table__row _type_segment(.)*?</tr>', sout)]
        indexesEvent = [[m.start(), m.end(), 1] for m in re.finditer('<tr class=\"table__row"(.)*?</tr>', sout)]
        indexesBlockedEvent = [[m.start(), m.end(), 1] for m in
                               re.finditer('<tr class=\"table__row _state_blocked"(.)*?</tr>', sout)]
        indexes = sorted(indexesSegment + indexesEvent + indexesBlockedEvent, key=lambda x: x[0])

        flLine = 0
        segmentId = ''
        for ind in indexes:
            if ind[2] == 0:
                flLine = 0
                if sout[ind[0]:ind[1]].find('sport_{}'.format(sport)) != -1:
                    flLine = 1
                    s = sout[ind[0]:ind[1]].split('<span class="table__title-text"')[1]
                    segmentId = s.split('>')[1].split('<')[0]
                    print(segmentId)
            if flLine == 1:
                if segmentId != '':
                    events_data.append([segmentId, sout[ind[0]:ind[1]]])
        print(len(events_data))
        return events_data

    @staticmethod
    def scrap(driver, sport='3088'):
        events_data = []
        try:
            tt = None
            all_events = '''//div//h1[contains(text(), 'Все события')]'''
            sport_filter_init = '''//div//h1[contains(text(), '{}')]'''.format(SportName.names[sport])
            sport_filter = '''//div[contains(text(), '{}')]'''.format(SportName.names[sport])

            try:
                tt = driver.find_element_by_xpath(sport_filter_init)
            except:
                pass

            if tt is None:
                print('try click')
                driver.find_element_by_xpath(all_events).click()
                print('click')
                try:
                    tt = driver.find_element_by_xpath(all_events + '/..' + sport_filter)
                    print('find tt')
                    tt.click()
                except:
                    tt = None

            if tt:
                lineTable = driver.find_element_by_xpath(
                    '//div[@class="table__flex-container"]'
                    '/table[@class="table"]'
                )
                print('lineTable - ok')
                sout = lineTable.get_attribute('outerHTML')
                print(len(sout))

                # for e in driver.find_elements_by_xpath(
                #         '//div[@class="table__btn icon _type_normal _icon_arrow-right-gray _state_collapsed"]'):
                #     e.click()
                # for e in driver.find_elements_by_xpath('//span[@class="table__event-details-icon"]'):
                #     e.click()
                # time.sleep(100)

                events_data = BKFonLiveScraper.parse(sout, sport=sport)
            else:
                driver.find_element_by_xpath(all_events).click()
                print('no table-tennis')

        except Exception as e:
            return events_data, e

        return events_data, None


class BKFonFileWriter:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def write(self, events_data, cur_time):
        try:
            last_event_id = ''
            fout = None
            for e in events_data:
                if e[0] != last_event_id:
                    last_event_id = e[0]
                    if fout:
                        fout.close()
                    if e[0] != 'error':
                        e[0] = e[0]
                    dir_path = os.path.join(self.data_dir, cur_time[:10])
                    if not os.path.exists(dir_path):
                        os.mkdir(dir_path)
                    fout = open(os.path.join(dir_path, e[0] + '.txt'), 'a', encoding='utf-8')
                fout.write('{}\t{}\n'.format(cur_time, e[1]))
            if fout:
                fout.close()
        except Exception as exc:
            print('file writing error')
            print(exc)
            try:
                fout.close()
            except:
                pass


class BKFonDBWriter:
    def __init__(self, con, table):
        self.con = con
        self.table = table

        if self.con:
            self.cur = self.con.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS {}
                (id SERIAL PRIMARY KEY, datetime timestamp, evendId INTEGER, compname TEXT, info TEXT)'''.format(table))
        self.con.commit()

    def write(self, events_data, cur_time, parser):
        try:
            block = []
            for e in events_data:
                if e[0] != 'error':
                    block.append(e[1])

            for matchBet in parser.addLineBlock(cur_time, block):
                print(matchBet)
                try:
                    info = '\t'.join([';'.join(matchBet.names[0]),
                                      ';'.join(matchBet.names[1]),
                                      json.dumps(matchBet.eventsInfo, ensure_ascii=False)])
                    info = info.replace("'", '"')
                    if self.con:
                        self.cur.execute(
                            "INSERT INTO {} (datetime,evendId,compname,info) VALUES('{}','{}','{}','{}')".
                                format(self.table, cur_time, matchBet.eventId, matchBet.compName, info)
                        )
                except psycopg2.DatabaseError as e:
                    print('Error %s' % e)
            if self.con:
                self.con.commit()
        except Exception as exc:
            print('db writing error')
            print(exc)


class BKFonScraperEngine:
    def __init__(self, url,
                 driver: Driver,
                 file_writer: BKFonFileWriter=None,
                 db_writer: BKFonDBWriter=None,
                 sport='3088',
                 active_timeout=5, passive_timeout=60,
                 driver_name='Chrome'):
        self.url = url
        self.file_writer = file_writer
        self.sport = sport
        self.db_writer = db_writer
        self.driver = driver
        self.driver_name = driver_name

        self.active_timeout = active_timeout
        self.passive_timeout = passive_timeout
        self.equal_cnt_threshold = 16

    def run(self):
        self.driver.run(self.url, sleep_time=5, is_random=1)

        k = 0
        k_error = -1
        error_cnt = 0
        equal_cnt = 0

        last_events_data = []

        parser = BKFonLiveParserNew(maxCnt=-1, sport=self.sport)
        while True:
            print((k, equal_cnt))
            k += 1
            timeout = self.passive_timeout

            if equal_cnt == self.equal_cnt_threshold:
                self.driver.run(self.url, sleep_time=5, is_random=1)
                equal_cnt = 0

            cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            events_data, exc = BKFonLiveScraper.scrap(self.driver.driver, sport=self.sport)

            if len(events_data) > 0:
                timeout = self.active_timeout

            if exc:
                # raise
                events_data.append(['error', 'error2\n' + str(exc)])
                print('error2')
                print(str(exc))

                if k_error == k - 1:
                    error_cnt += 1
                else:
                    error_cnt = 1
                    timeout = self.active_timeout
                if error_cnt == 5:
                    timeout = self.passive_timeout
                    error_cnt = 0
                k_error = k

                print('driver1')
                try:
                    print('driver2')
                    self.driver.run(self.url, sleep_time=5, is_random=1)
                except Exception as eee:
                    print('EXC')
                    print(eee)
                    pass

            if '\t'.join([e[1] for e in events_data]) == '\t'.join([e[1] for e in last_events_data]):
                equal_cnt += 1
            else:
                equal_cnt = 0
            last_events_data = events_data.copy()

            self.file_writer.write(events_data, cur_time)
            if self.db_writer:
                self.db_writer.write(events_data, cur_time, parser)

            time.sleep(timeout)


def main():
    pass

if __name__ == "__main__":
    main()
