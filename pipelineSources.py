from Logger import Logger

from MasterTourScraper import MasterTourScraper
from MasterTourParser import MasterTourParser
from MasterTourPreparator import MasterTourPreparator

from LigaProScraper import LigaProScraper
from LigaProParser import LigaProParser
from LigaProPreparator import LigaProPreparator
from LigaProChecker import LigaProChecker

from ChallengerSeriesScraper import ChallengerSeriesScraper
from ChallengerSeriesParser import ChallengerSeriesParser
from ChallengerSeriesPreparator import ChallengerSeriesPreparator

from BKFonResultsScraper import BKFonResultsScraper
from BKFonResultsParser import BKFonResultsParser
from BKFonResultsPreparator import BKFonResultsPreparator

from RttfScraper import RttfScraper
from RttfParser import RttfParser
from RttfPreparator import RttfPreparator

from IttfScraperParser import IttfParser
from IttfPreparator import *

import kchr_prepare


def scrap():
    LigaProScraper.run(logger=Logger('LigaProScraper.txt'))
    LigaProScraper.run(logger=Logger('LigaProScraper.txt'), mode='games')
    MasterTourScraper.run(logger=Logger('MasterTourScraper.txt'))
    ChallengerSeriesScraper.run(logger=Logger('ChallengerSeriesScraper.txt'))
    BKFonResultsScraper.run(logger=Logger('BKFonResultsScraper.txt'))
    RttfScraper.run(logger=Logger('RttfScraper.txt'))


def parse():
    LigaProParser.run(logger=Logger('LigaProParser.txt'))
    MasterTourParser.run(logger=Logger('MasterTourParser.txt'))
    ChallengerSeriesParser.run(logger=Logger('ChallengerSeriesParser.txt'))
    BKFonResultsParser.run(logger=Logger('BKFonResultsParser.txt'))
    RttfParser.run(logger=Logger('RttfParser.txt'))
    #IttfParser.run(logger=Logger('IttfParser.txt'))


def prepare():
    LigaProPreparator.run(logger=Logger('LigaProPreparator.txt'))
    MasterTourPreparator.run(logger=Logger('MasterTourPreparator.txt'))
    ChallengerSeriesPreparator.run(logger=Logger('ChallengerSeriesPreparator.txt'))
    BKFonResultsPreparator.run(logger=Logger('BKFonResultsPreparator.txt'))
    RttfPreparator.run(logger=Logger('RttfPreparator.txt'))
    IttfPreparator.run(logger=Logger('IttfPreparator.txt'))
    # kchr_prepare.main()

def check():
    LigaProChecker.run(logger=Logger('LigaProChecker.txt'))

def main():
#    IttfParser.run()
#    RttfScraper.run(logger=Logger('RttfScraper.txt'))

    scrap()
    parse()
    prepare()
    check()

if __name__ == "__main__":
    main()