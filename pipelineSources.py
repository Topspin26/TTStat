from Logger import Logger

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

from RttfScraper import RttfScraper
from RttfParser import RttfParser
from RttfPreparator import RttfPreparator

from IttfScraperParser import IttfParser
from IttfPreparator import *


def scrap():
    #LigaProScraper.run(logger=Logger('LigaProScraper.txt'))
    #MasterTourScraper.run(logger=Logger('MasterTourScraper.txt'))
    #ChallengerSeriesScraper.run(logger=Logger('ChallengerSeriesScraper.txt'))
    BKFonResultsScraper.run(logger=Logger('BKFonResultsScraper.txt'))
    RttfScraper.run(logger=Logger('RttfScraper.txt'))


def parse():
    LigaProParser.run(logger=Logger('LigaProParser.txt'))
    MasterTourParser.run(logger=Logger('MasterTourParser.txt'))
    ChallengerSeriesParser.run(logger=Logger('ChallengerSeriesParser.txt'))
    BKFonResultsParser.run(logger=Logger('BKFonResultsParser.txt'))
    RttfParser.run()
    IttfParser.run()


def prepare():
    LigaProPreparator.run(logger=Logger('LigaProPreparator.txt'))
    MasterTourPreparator.run(logger=Logger('MasterTourPreparator.txt'))
    ChallengerSeriesPreparator.run()
    BKFonResultsPreparator.run()
    RttfPreparator.run()
    IttfPreparator.run()


def main():
#    IttfParser.run()
#    scrap()
    parse()
    prepare()

if __name__ == "__main__":
    main()