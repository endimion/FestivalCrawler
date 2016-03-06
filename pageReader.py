#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2

class pageNode:
    # This class defines the structure of an HTML node
    # of the form <tag> content </tag>
    # it stores the type of the class, i.e. div, p, a, etc.
    # and the father of it
    # also it stores all of the children nodes of that tag as an array

    #father = None
    #kids = []
    #content=""
    #name=""
    #isClosed = False

    def __init__(self, name,content):
        self.name = name
        self.content = content
        self.kids = []
        self.father = None
        self.isClosed = False

    def add_father(self, father):
        self.father = father

    def add_child(self, child):
        self.kids.append(child)

    def close(self):
        self.isClosed= True

    def __str__(self):
        return "NAME: " + self.name + "\n CLOSED: " +  str(self.isClosed) + "\n CHILDREN:: " + str(self.kids) + "\n CONTENTS:: " +self.content




class PageParser:
    # This objects allows the functionality of parsing an HTML page
    # and storing its items

    url=""
    nodes = []
    # regex for html opening and closing tags respectively
    # and one line tags line <a href="" />
    opening_tag_reg = "(<(?!/)(.*?)>)"
    closing_tag_reg = "(</(.*?)>)"
    one_line_reg = "<(.*?)/>"


    def __init__(self, url):
        self.url = url
        self.nodes = []



    def findFather(self):
        # iterates through the nodes of the nodes array
        # to find the last one that is not a closing node
        # and returns the nod
        for node in reversed(self.nodes):
            if not node.isClosed :
                #print "Father will be set to  " + str(node.name)
                return node

        return None


    def findNodeToClose(self,name):
        # scans the nodes stored from last to first
        # for the one matching the given type
        # that is not closed and
        # closes it
        for nod in reversed(self.nodes):
            if nod.name == name and not nod.isClosed:
                nod.isClosed = True



    def makeNode(self,reg,string):
        m = re.search(reg,string)
        main_tag = string[m.start():m.end()]

        tag_name = main_tag.replace("</","").replace(">","").replace("<","")




        rest = string[m.end():]
        c = re.search( "<", rest) # find the first opening < in the line
        #print "main tag is " + main_tag

        node = pageNode(tag_name,"")
        if c:
            additional_tags = rest[c.end()-1:]
            contents = rest[:c.start()]
            node.content = contents
            #print "contents is " + contents
        else:
            additional_tags = rest

        # if the line is not only one tag


        if len(additional_tags) > 1:
            self.matchAndStore(additional_tags)

        # find the father of the node
        node.father = self.findFather()

        #self.nodes.append(node)
        return node




    def matchAndStore(self,string):
        p_oneline = re.compile('^< [^<]*/>$')
        p_openning = re.compile("(<(?!/)(.*?)>)")
        p_closing = re.compile("(</(.*?)>)")


        contents_reg = "(.*?!<)"
        the_string = string.strip()

        # flag to denote if the string was a node
        the_node = None

        if p_oneline.search(the_string):
            print " ONE LINE!!! " + the_string
        else:
            if p_openning.match(the_string):
                #print " opening " + the_string
                the_node = self.makeNode("(<(?!/)(.*?)>)",the_string)
            else:
                if p_closing.match(the_string):
                    #print " closing " + the_string
                    the_node = self.makeNode("(</(.*?)>)",the_string)
                    the_node.isClosed = True
                else:
                    # in this case the line is neither opening nor closing a tag
                    # so it is a simple string, i.e. a content for the previously opened
                    # tag
                    if len(self.nodes) > 0:
                        self.nodes[len(self.nodes)-1].content = the_string


        if the_node != None:
            self.findNodeToClose(the_node.name)
            self.nodes.append(the_node)







    def parseUrl(self):
        try:
            data = urllib2.urlopen(self.url)

            for line in data :
                line = line.strip()
                self.matchAndStore(line)

            data.close()

            print len(self.nodes)
        except:
            print "could not read url " + self.url



        # then we scan all the nodes to add the children to their fathers
        for node in self.nodes:
           for child in self.nodes:
                if child.father == node:
                    node.add_child (child)


