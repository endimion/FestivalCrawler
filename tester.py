#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pageReader import PageParser
from Crawler import FestCrawler


_url = "http://www.math.ntua.gr/~sofia"
##pReader = PageParser(_url)
#pReader.parseUrl()
spider = FestCrawler()
#spider.searchPage(_url)

#spider.clearAll()
_url="http://www.tinostoday.gr/2015/07/2015_24.html"
#spider.searchPage(_url)

_url = "http://www.chiosphotofestival.gr/"
#spider.searchPage(_url)

_url = "http://www.lathra.gr/"
#spider.searchPage(_url)

_url = "http://www.ireon-music-festival-samos.gr/gr/"
spider.searchPage(_url, "Samos")

_url = "http://www.chaniarockfestival.gr/"
spider.searchPage(_url, "chania")

_url = "http://www.kosinfo.gr/events"
spider.searchPage(_url,"Kos")

_url = "http://www.greeka.com/cyclades/ios/ios-festivals.htm"
spider.searchPage(_url,"Ios")

_url = "http://www.parospark.com/festival-at-the-park/"
spider.searchPage(_url,"Paros")

_url = "http://www.stimarpissa.gr/"
spider.searchPage(_url,"Πάρο")

_url = "http://parospress.blogspot.gr/2015/09/paris-paros_30.html"
spider.searchPage(_url,"Πάρο")