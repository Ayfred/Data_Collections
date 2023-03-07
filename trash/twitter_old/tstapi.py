
import tweepy
import pandas as pd
import time


consumer_key = "OZCcR4AMZkQUBWfd7AzV4gZJ9" #Your API/Consumer key 
consumer_secret = "TWw2tWYFhsgqAEkOcr68BZRZN2Hqq7Etr5l5jaBuPOKqqMF8Gk" #Your API/Consumer Secret Key
access_token = "2149296548-poLAVAiA9144SOGHy3bOwaGVNX0pGvYh98Avhkh"    #Your Access token key
access_token_secret = "BQyr8K2d59RV2B646q3ZmphXL5Xw3a25Gt04kBXCCCc7u" #Your Access token Secret key

#Pass in our twitter API authentication key
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

#Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)


username = "john"
no_of_tweets =10


try:
    #The number of tweets we want to retrieved from the user
    tweets = api.user_timeline(screen_name=username, count=no_of_tweets)
    
    #Pulling Some attributes from the tweet
    attributes_container = [[tweet.created_at, tweet.favorite_count,tweet.source,  tweet.text] for tweet in tweets]

    #Creation of column list to rename the columns in the dataframe
    columns = ["Date Created", "Number of Likes", "Source of Tweet", "Tweet"]
    
    #Creation of Dataframe
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
except BaseException as e:
    print('Status Failed On,',str(e))
    time.sleep(3)

print(tweets_df)

