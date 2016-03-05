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
            print "added " + url
            self.pagesToSearchNext.append(url)


    def searchForImage(self,node,festival, _url):
        m = re.search('(?<=src=\')(.*?\')?', node.name.replace("\"","\'"))
        if m:
            festival.img.append(m.group(0))
            #print  festival.img



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



        keywords = ["Φεστιβάλ","φεστιβάλ", "Festival", "festival"]
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
                        for child in node.kids:
                            if "img" in child.name:
                                self.searchForImage(child,festival,url)
                                break

                        # if no image was found then we search the siblings
                        if festival.img =="":
                            for sibling in node.father.kids:
                                if "img" in sibling.name:
                                    #print "found an image inside sibling " + sibling.name
                                    self.searchForImage(sibling,festival,url)
                                    break
                        # finally the festival is added to the list of festivals
                        festivals.append(festival)
                    else:
                        # the keyword was found probably found inside a link
                        # if there is a url in the node
                        if "href" in node.name:
                             self.searchForLink(node)








        cleaned_fests = []

        for fest in festivals:
            if not(fest.name == "" and fest.url == "" and fest.date=="" and fest.img==""):
                cleaned_fests.append(fest)


        for fest in cleaned_fests:
            print fest