from os import walk
import datetime
from bs4 import BeautifulSoup


class ChallengerSeriesParser:

    @staticmethod
    def run():
        for f in walk('data/challenger_series/results_raw'):
            for ff in sorted(f[2]):
                print(ff)
                sKey, lines = ChallengerSeriesParser.parse('data/challenger_series/results_raw/' + ff)
                print(sKey)
                with open('data/challenger_series/results/' + sKey + '.txt', 'w', encoding='utf-8') as fout:
                    fout.write(lines)

    @staticmethod
    def parse(filename):
        soup = BeautifulSoup(open(filename, encoding='utf-8').read(), "lxml")
        startDate = filename.split('/')[-1].split('_')[0]

        trs = soup.find(class_='rounds').find_all('tr')
        days = {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}
        fl = -1
        rows = []

        for tr in trs[2:-1]:
            tds = tr.find_all('td')
            if tds[0].text.replace('<strong>', '').replace('</strong>', '') in days:
                fl += 1
            t = tds[1].text
            score = tds[3].text.replace(':', '-')
            t = t.replace('18:300', '18:30').replace('28:40', '18:40')
            if t.lower() == 'cancel' or score.lower() == 'cancel' or t.lower() == 'injure':
                continue
            name1 = tds[4].text.replace(',', '').replace('<strong>', '').replace('</strong>', '')
            name2 = tds[5].text.replace(',', '').replace('<strong>', '').replace('</strong>', '')
            tt = ''
            mdt = (datetime.datetime.strptime(startDate, "%Y-%m-%d") + datetime.timedelta(days=fl)).strftime("%Y-%m-%d")
            if t != '-':
                curDate = (datetime.datetime.strptime(startDate + ' ' + t, "%Y-%m-%d %H:%M") + datetime.timedelta(
                    days=fl) + datetime.timedelta(hours=2))
                mdt = curDate.strftime("%Y-%m-%d")
                tt = curDate.strftime("%H:%M")
            rows.append('\t'.join([mdt, tt, name1, name2, score]))
        tid = filename.split('/')[-1][:-4]
        return tid, '\n'.join(rows)


def main():
    ChallengerSeriesParser.run()

if __name__ == "__main__":
    main()