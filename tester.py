from pageReader import PageParser
from Crawler import FestCrawler


_url = "http://www.math.ntua.gr/~sofia"
##pReader = PageParser(_url)
#pReader.parseUrl()
spider = FestCrawler()
spider.searchPage(_url)