#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import urllib
from Crawler import FestCrawler
import traceback



festival_dict = {"":[]}


def main():
    islands = ["Paros","Πάρος","Naxos", "Νάξος"]
    keywords = ["Festival ", "Φεστιβάλ "]

    for island in islands:
        for keyword in keywords:

            query = urllib.urlencode({'q': keyword + island})
            #print str(query)

            spider = FestCrawler()
            search_res_indexes = [ x*8 for x in range(0,3)] # the google api returns the results in groups of 8 res
            num_of_searches = 0

            island_res = []
            for i in search_res_indexes:
                # so here i goes from 0,8,16,32 to get the first 32 search results
                url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&%s&start=%d'% (query,i)

                search_response = urllib.urlopen(url)
                search_results = search_response.read()
                results = json.loads(search_results)
                # print the json to see what is going on
                #print json.dumps(results, indent=4, sort_keys=True)
                #break

                if not results['responseStatus'] == 403:
                    data = results['responseData']
                    if not type(data) == "NoneType":
                        try:
                            hits = data['results']
                            for hit in hits:
                                url = hit['url']
                                print "will search in search result ", url, " this is search number ", num_of_searches
                                num_of_searches +=1
                                island_res.append(spider.searchPage(url,island))

                        except:
                            traceback.print_exc()
                            print "something wrong with the results"
                    else:
                        print "data type is None"

                else:
                    print("google wont let us search any more!!!")
            festival_dict[island] = island_res

            # finally print the results
            for key in festival_dict.keys():
                print "festivals of ", key
                for fest_list in festival_dict[key]:
                    for fest in fest_list:
                        try:
                            print fest
                        except:
                            pass


if __name__ == "__main__":
    main()