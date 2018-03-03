
from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

MONGO_HOST= 'mongodb://localhost/twitterdb'  

WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']

CONSUMER_KEY = "Key"
CONSUMER_SECRET = "Secret"
ACCESS_TOKEN = "Token"
ACCESS_TOKEN_SECRET = "Token_Secret"

class StreamListener(tweepy.StreamListener):. 
    def on_connect(self):
        print("You are now connected to the streaming API.")
    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False
    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            db = client.twitterdb
            datajson = json.loads(data)
            created_at = datajson['created_at']
            if("extended_tweet" in datajson):
                tweet = datajson['extended_tweet']['full_text']
                print("Tweet collected at " + str(created_at))
                print(tweet)
                db.lang_tweets.insert(datajson)
        except Exception as e:
            print(e)

while(True):
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
        streamer = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')
        streamer.filter(languages=["en"], track=["the"])
        #streamer.filter(locations=[-180,-90,180,90])
    except Exception as e:
        print(e)







