import re
from textblob import TextBlob
def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

tweet=clean_tweet('Small Business: Do You Have A Dream? http://ow.ly/ocZE1 #smbiz #usguys #mlk (@heidicohen)')
print(tweet[0:5])


def get_tweet_sentiment(tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

