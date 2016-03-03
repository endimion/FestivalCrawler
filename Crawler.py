from pageReader import PageParser, pageNode

class FestCrawler:



    def searchPage(self,url):


        parser = PageParser(url)
        parser.parseUrl()
        the_nodes = parser.nodes

        keywords = ["Φεστιβάλ", "Festival", "φεστιβάλ", "festival"]


        for node in the_nodes:
            for keyword in keywords :
                if keyword in node.contents:
                    print " matching tag found"
