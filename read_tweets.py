from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
import re
from nltk.corpus import stopwords
#from fetch_tweets import *
import os
from nltk.tag import StanfordNERTagger
from news import *
from tweepy import OAuthHandler

#connecting with MongoDB
MONGO_HOST= 'mongodb://localhost/twitterdb'  
news_dict={}
tweets_dict={}

MONGO_HOST= 'mongodb://localhost/twitterdb'
client = MongoClient(MONGO_HOST)

# Use twitterdb database. If it doesn't exist, it will be created.
db = client.twitterdb
collection = db.test

client = MongoClient(MONGO_HOST)
db = client.twitterdb


CONSUMER_KEY = "Key"
CONSUMER_SECRET = "Secret"
ACCESS_TOKEN = "Token"
ACCESS_TOKEN_SECRET = "Token_Secret"



def insert_tweets_mongo(data):
    try:
        db.words_tweets.insert(data)
    except Exception as e:
        print(e)


def insert_news_mongo(data):
    try:
        #datajson = json.loads(data) already done
        db.words_news.insert(data)
    except Exception as e:
        print(e)

def clean_tweet(tweet):
        str= re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweet)
        str_split=str.split()
        stop_words = set(stopwords.words('english'))
        final_sentence = [w for w in str_split if not w in stop_words]
        return final_sentence
        


#import Algorithmia
#client2=Algorithmia.client('simxOBDJv9IAgZRrv4JFjmBFkWe1')
#def get_ner(tweet):
    #ner_algo=client2.algo('StanfordNLP/NamedEntityRecognition/0.1.1').set_options(timeout=600)
    #ner_result=ner_algo.pipe(tweet).result
    #return ner_result


st=StanfordNERTagger('/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/stanford-ner-2014-06-16/stanford-ner.jar')

#java_path = "C:/Program Files/Java/jdk1.8.0_131/bin/java.exe"
#os.environ['JAVAHOME'] = java_path


accepted_tags=['LOCATION','ORGANIZATION','PERSON','GPE','FACILITY']

#retuns a list of words sorted on frequency after NER
def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux

#returns a search_list based on most common Named Entities
def get_NERS(document):
    tweet=document['extended_tweet']['full_text']
    cleaned_tweet=clean_tweet(tweet)
    print("cleaning the tweet")
    print(cleaned_tweet)
    print("Performing NER on tweet")
    tagged_list=st.tag(cleaned_tweet)
    
    print(tagged_list)
    
    dict={}
    
    for l in tagged_list:
        if l[1] in accepted_tags:
            if l[0] in dict:
                dict[l[0]]+=1
            else:
                dict[l[0]]=1
    
    temp=sortFreqDict(dict)
    search_list=[l[1] for l in temp]
    
    dict1={}
    for l in tagged_list:
        if l[1]=='O':
            
            if l[0] in dict1:
                dict1[l[0]]+=1
            else:
                dict1[l[0]]=1
    
    temp=sortFreqDict(dict1)
    for l in temp:
        search_list.append(l[1])
    
    print(" 5 most common NERs: ")
    print(search_list[0:5])
    return (search_list)


#fetches newsarticles based on query
def news_search(search_list):
    for s in search_list[0:5]:
        news= get_news(s)
        insert_news_mongo(news)
        news_dict[s]=news



# create OAuthHandler object
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# set access token and secret
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# create tweepy API object to fetch tweets
api = tweepy.API(auth)



#searches tweets based on query
def search_tweets(query):
    while(True):
        try:
            print("Fetching and inserting into database tweets with query-> "+query)
            fetched_tweets = api.search(q=query, count = 10,lang='en',tweet_mode='extended')
            return fetched_tweets
        except:
            print("Fetching")


def fetch_tweets_news():
    for document in collection.find():
        search_list=get_NERS(document)
        print("****Searching relevant tweets using Named entities found*****")
        for s in search_list[0:5]:
            tweet_list=search_tweets(s)
            for tweet in tweet_list:
                insert_tweets_mongo(tweet._json)
            tweets_dict[s]=tweet_list
            
        print("****Searching relevant news using Named entities found****")
        news_search(search_list) #finding relevant news articles with the NEs found
    
    return tweets_dict


fetch_tweets_news()






