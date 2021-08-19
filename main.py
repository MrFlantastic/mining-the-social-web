### This is the file to test our Twitter API scripts
import tweepy
import pandas

customer_key = 'zRJho8P4ptqQ0NhAkSnaHoTZA'
customer_secret = '8GXu21P5uvMKo6yzyyUIMKwHgCKq3unDgSp6n26wFGuMEx5pLI'
access_token = '486977981-V0Uew4va809LRG8pVhvzy11npJ0Vv4kTQkbCepIP'
access_token_secret= 'XgAQtKGfnAApXuoRouybXnjw4qehvQwySftMiA1C0l0IJ'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

