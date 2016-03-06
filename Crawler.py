#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pageReader import PageParser, pageNode
import re
from MLStripper import MLStripper

class Festival:

    def __init__(self,name,url,img,date):
        self.name = name
        self.url = url
        self.date = date
        self.img = []

    def __str__(self):
        return "Festival name: " + self.name + " URL: " + self.url + " Image: "+ str(self.img) + " Date " + self.date




class FestCrawler:

    def __init__(self):
        self.the_nodes=[]
        self.pagesToSearchNext = [] # stores the pages we will search next
        self.imgReg = re.compile('(?<=src=\')(.*?((.jpg)|(.png))\')?')
        self.altReg = re.compile('(?<=alt=\')(.*?\')?')
        self.keywords =["Φεστιβάλ","φεστιβάλ", "Festival", "festival"]
        self.months = [ "January","February","March","April","May","June","July","August","September","October",
                        "November","December","Ιανουάριος","Φεβρουάριος","Μάρτιος",
                        "Απρίλιος","Μάιος","Ιούνιος","Ιούλιος","Αύγουστος","Σεπτέμβριος","Οκτώβριος","Νοέμβριος","Δεκέμβριος"
                        ,"Ιανουαρίου","Φεβρουαρίου","Μαρτίου","Απριλίου","Μαίου","Ιουνίου","Σεπτεμβρίου","Οκτωβρίου","Νοεμβρίου","Δεκεμβρίου"]
        monthRegList = [ "([0-9][0-9])+ \s"+ m + "[0,9]{4}" for m in self.months]
        monthRegExpr = "|".join(monthRegList)
        self.monthReg = re.compile(monthRegExpr)


    def strip_tags(self,html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()




    def searchForLink(self, node):
        # checks the name of the node to see if it contains
        # a link element, i.e. href
        # if it does then the link from the tag is added to the queue to
        # search in

        m = re.search('(?<=href=\')(.*?\')?', node.name)
        if m:
            url = m.group(0).replace("\'","")
            print "url to search next, added: " + url
            self.pagesToSearchNext.append(url)


    def searchAndStoreImage(self,node,festival, _url):
        # searches the give nod for an img tag
        # next if an alt attribute is contained then if that contains
        # a keyword in the description, then the link for the img is added to the
        # list of imgs of the festival
        m = self.imgReg.search(node.name.replace("\"","\'"))
        if m:
            #print "image found "
            if "alt" in node.name:
                # if the image contains an alt description then that should include
                # logically the name of the island and the keyword festival
                alt = self.altReg.search(node.name.replace("\"","\'"))
                #print "image contains alt  " + alt.group(0)
                for key in self.keywords:
                    if key in alt.group(0):
                        #print "IMG WILL BE ADDED"
                        if len(m.group(0)) > 5 :
                            # if the length of the img path is more than 5 characters
                            festival.img.append(m.group(0))
            return node
        else:
            return None
            #print  festival.img



    def searchTreeForImg(self,node, festival, url):
        # search the node and all of its children  for an
        # for  an img element and add these to the images of the festival
        # if no such descendant is found None is returned
        res = self.searchAndStoreImage(node,festival,url)
        for child in node.kids:
            res = self.searchTreeForImg(child,festival,url)
        return None


    def searchPage(self,url, island):
        # searches the url for nodes that contain the keywords festival etc.
        # then for each such node we create a new Festival object
        # that contains the information about the festival such as,
        # url, date, and an image about the festival

        # Algorithm:
        # A .if the festival keyword is found in a link and not in a div etc.
        # then the link is pushed to a queue and the link is visited next
        #
        # B. If the festival is found inside a div etc. then
        # we have found a page that contains information about the festival
        # thus as its link we add the current page we are visiting
        # the festival name gets set to the name found inside the <tag>
        # and as images we add all the potential images found

        parser = PageParser(url)
        parser.parseUrl()
        self.the_nodes = parser.nodes
        festivals = []



        keywords = ["Φεστιβάλ ","φεστιβάλ ", "Festival ", "festival ","Festivals ","festivals "]
        #keywords = [ ",".join([c + " " + island, island +" "+c]) for c in keywords]

        for node in self.the_nodes:

            for keyword in keywords :

                if (keyword in node.content and island in node.content) or (keyword in node.name and island in node.name):

                    if keyword in node.content:
                        # if the keyword was found in the content of a node
                        # then this page will likely contain info about a festival
                        # so we create a new festival object
                        festival = Festival(node.content,url,"","")

                        # search the children of the node for image elements:
                        imgTag = self.searchTreeForImg(node,festival,url)


                        # if no image was found then we search the siblings and their children
                        if len(festival.img) == 0:
                            for sibling in node.father.kids:
                                self.searchTreeForImg(sibling,festival,url)

                        festivals.append(festival)
                    else:
                        # the keyword was found probably found inside a link
                        # if there is a url in the node
                        if "href" in node.name:
                             self.searchForLink(node)

        #search the newly added urls
        # for festivals
        for new_url in self.pagesToSearchNext:
            print "will look in page " + new_url
            self.pagesToSearchNext.remove(new_url)
            self.searchPage(new_url,island)


        cleaned_fests = []

        for fest in festivals:
            if not(fest.name == "" and fest.url == "" and fest.date=="" and fest.img==""):
                cleaned_fests.append(fest)


        for fest in cleaned_fests:
            print fest