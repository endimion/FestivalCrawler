import requests
import json
import urllib
from Crawler import FestCrawler




def main():

    island = "Paros"
    query = urllib.urlencode({'q': 'Festival'+island})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'% query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    # print the json to see what is going on
    # print json.dumps(results, indent=4, sort_keys=True)
    spider = FestCrawler()

    if not results['responseStatus'] == 403:
        data = results['responseData']
        if not type(data) == "NoneType":
            try:
                hits = data['results']
                for hit in hits:
                    url = hit['url']
                    print "will search in search result ", url
                    spider.searchPage(url,island)

            except:
                print "something wrong with the results"
        else:
            print "data type is None"

    else:
        print("google wont let us search any more!!!")



if __name__ == "__main__":
    main()