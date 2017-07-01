from MasterTourScraper import MasterTourScraper
from MasterTourParser import MasterTourParser
from MasterTourPreparator import MasterTourPreparator

from LigaProScraper import LigaProScraper
from LigaProParser import LigaProParser
from LigaProPreparator import LigaProPreparator

from ChallengerSeriesScraper import ChallengerSeriesScraper
from ChallengerSeriesParser import ChallengerSeriesParser
from ChallengerSeriesPreparator import ChallengerSeriesPreparator

from BKFonResultsScraper import BKFonResultsScraper
from BKFonResultsParser import BKFonResultsParser
from BKFonResultsPreparator import BKFonResultsPreparator


def scrap():
    LigaProScraper.run()
    MasterTourScraper.run()
    ChallengerSeriesScraper.run()
    BKFonResultsScraper.run()


def parse():
    LigaProParser.run()
    MasterTourParser.run()
    ChallengerSeriesParser.run()
    BKFonResultsParser.run()


def prepare():
    LigaProPreparator.run()
    MasterTourPreparator.run()
    ChallengerSeriesPreparator.run()
    BKFonResultsPreparator.run()


def main():
    #scrap()
    #parse()
    prepare()

if __name__ == "__main__":
    main()