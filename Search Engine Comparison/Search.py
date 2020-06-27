from bs4 import BeautifulSoup
import time
import requests
import json
from random import randint
from html.parser import HTMLParser
from urllib.parse import unquote

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64 ;x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep:
            #num = 5
            num = randint(5, 10)
            #print("Sleep Time:", num)
            time.sleep(num)
        temp_url = '+'.join(query.split())
        #temp_url = query
        url = [search_engine_url]?p=' + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, 'html.parser')
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        #print(soup)
        raw_results = soup.find_all("a", {"class": "ac-algo fz-l ac-21th lh-24"})
        results = []
        top10results = []
        print(len(raw_results))
        if len(raw_results) > 10:
            top10results = raw_results[:10]
        else:
            top10results = raw_results
        print(len(top10results))
        # implement a check to get only 10 results and also check that URLs must not be duplicated
        filetemp = open('temp.txt', 'w')

        for result in top10results:
            link = result.get('href')
            temp = []
            temp = link.split("/RU=")
            if len(temp) == 1:
                link = unquote(link)
                #print(link)
            else:
                temp = temp[1].split("/RK")
                link = unquote(temp[0])
                #filetemp.write(link)
                #filetemp.write('\n')
            results.append(link)
            print(link)
        print(len(results))

        filetemp.close()
        return results


    #write data to a json file without ?
    @staticmethod
    def getQueries():
        query_dict = {}
        with open("queries.txt", 'r') as file:
            while True:
                query = file.readline()
                if not query:
                    break
                query = query.split(' ?')[0]
                query_results = SearchEngine.search(query)

                query_dict[query] = query_results
                query = ""
                #print(query_dict)

        file.close()

        with open('yahooResult.json', 'w') as result_file:
            json.dump(query_dict, result_file, ensure_ascii=False, indent=4)


# ############Driver code############
SearchEngine.search("How many miles are in africa ?")
#SearchEngine.getQueries()
# ###################################
