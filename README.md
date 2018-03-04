                                    ********************README**********************

Welcome!

COMPONENTS


  main.py                       - To collect 10K random tweets and store them in MongoDB instance using Twitter Streaming API
  
  read_tweets.py                - Reads tweets from Database, finds 5 most frequently used named entities from each of the 10K tweets
  
  news.py                       - To search news based on tags
  
  sentiment_analysis.py         - To perform sentiment analysis using Textblob
  
  twitterdb.zip                 - file containing collections:
  
                                    lang_tweets.bson    - containing initial 10K tweets
                                    
                                    words_tweets.bson   - has tweets contaning the named entities 
                                    
                                    words_news.bson     - has news collecting the named entities
  

RUNNING

In read_tweets.py provide CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN and ACCESS_TOKEN_SECRET for twitter application.
Import twitterdb Database (twitterdb.zip) into Mongo Client
  For command line, to collect tweets based on NER, invoke:

    > python read_tweets.py 
    
  For command line, to collect 10K tweets, invoke:
  
    > python main.py

  To run a single server database:

    $ sudo mkdir -p /data/db
    $ ./mongod
    $
    $ # The mongo javascript shell connects to localhost and test database by default:
    $ ./mongo
    > help

OTHER REQUIREMENTS

  Uses english.all.3class.distsim.crf.ser.gz and stanford-ner.jar (present in the same folder) for performing named entity recognition using Stanform Tool

