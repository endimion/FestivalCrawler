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
        #self.festivals = []


    def strip_tags(self,html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()




    def searchForLink(self, node, festival):
        # checks the name of the node to see if it contains
        # a link element, i.e. href
        # if it does then the link from the tag is retrieved and
        # stored at the given Festival object url attribute

        m = re.search('(?<=href=\')(.*?\')?', node.name)
        if m:
            festival.url = m.group(0).replace("\'","")
            #print festival.url


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

        parser = PageParser(url)
        parser.parseUrl()
        self.the_nodes = parser.nodes
        festivals = []

        keywords = ["Φεστιβάλ","φεστιβάλ", "Festival", "festival"]
        #keywords = [ ",".join([c + " " + island, island +" "+c]) for c in keywords]

        for node in self.the_nodes:

            for keyword in keywords :

                if (keyword in node.content and island in node.content) or (keyword in node.name and island in node.name):
                    #print " matching tag found-->" + str(node)
                    if keyword in node.content:
                        festival = Festival(node.content,"","","")
                    else:
                        name = self.strip_tags("<"+node.name +">")
                        festival = Festival(name,"","","")

                    # if there is a url in the node
                    if "href" in node.name:
                         self.searchForLink(node,festival)
                    else:
                        #print "will look inside the children of " + node.name   + " for href links" + str(len(node.kids))
                        #print node.content
                        # we try to find a link in the children of the father
                        for child in node.kids:
                            if "href" in child.name:
                                self.searchForLink(child,festival)
                                break

                        #if i didnt find a link in the children then i will look in the siblings
                        if festival.url == "":
                            for sibling in node.father.kids:
                                if "href" in sibling.name:
                                    self.searchForLink(sibling,festival)
                                    break

                    # search the children of the node for image elements:
                    for child in node.kids:
                        if "img" in child.name:
                            #print "found an image inside " + node.name
                            self.searchForImage(child,festival,url)
                            break

                    # if no image was found then we search the siblings
                    if festival.img =="":
                        for sibling in node.father.kids:
                            if "img" in sibling.name:
                                #print "found an image inside sibling " + sibling.name
                                self.searchForImage(sibling,festival,url)
                                break

                    festivals.append(festival)

        cleaned_fests = []
        for fest in festivals:
            if not(fest.name == "" and fest.url == "" and fest.date=="" and fest.img==""):
                cleaned_fests.append(fest)


        for fest in cleaned_fests:
            print fest