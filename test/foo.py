from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import random
import re


def main():
    s1 = '<tr style="display: table-row;" id="segment15435" class="trSegment"><td class="tdSegmentColor tdSegmentColorSport1"\
 colspan="16"><div class="divSegment"><div class="divSegmentSportImage sport1"></div><div class="lineSegmentFlag flag276</tr>'
    s2 = '<tr style="display: table-row;" id="segment15435" class="trSegment"><td class="tdSegmentColor tdSegmentColorSport1"\
 colspan="16"><div class="divSegment"><div class="divSegmentSportImage sport1"></div><div class="lineSegmentFlag flag276</tr>'
    s = s1 + s2
    print(s)
    indexes = [[m.start(), m.end(), 0] for m in re.finditer('<tr [^>]* id=\"segment(.)*?</tr>', s)]
    print(s.find('123'))
    print(indexes)
    

if __name__ == "__main__":
    main()