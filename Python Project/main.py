### This is the file to test our Twitter API scripts
import tweepy
import pandas as pd

customer_key = 'MJsP5vZzgMEBQJMViZ0I6R1bd'
customer_secret = 'IbhVV9yvGdBw9fjsce5aSZq5kazXnBR29fqLCD7H1WjzcpH03u'
access_token = '486977981-9vqd1VTICsY4i1HOFC0eBkvU2JUUXuxmjMS6nwwa'
access_token_secret = 'MTNvx5Fuula5Bqwo0iEqP0XMXB5nSgWipbTxtuAw4H4e3'

auth = tweepy.OAuthHandler(customer_key, customer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

me = api.get_user(screen_name = 'MrFlantastic')
me.id 