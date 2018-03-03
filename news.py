#collecting news corresponding to tag
import urllib
import json
from urllib.request import urlopen

def get_news(query):
    while(True):
        try:
            url=('https://newsapi.org/v2/everything?q='+query+'&apiKey=a09443b6fad947f09631f88876e8ecd6')
            #url=('https://newsapi.org/v2/everything?q=bitcoin&apiKey=a09443b6fad947f09631f88876e8ecd6')
            f = urlopen(url)
            json1 = json.loads(f.read())
            print("The headline of first article fetched "+json1['articles'][0]['title'])
            return json1
        except:
            print("Trying again")



#get_news('trump')
