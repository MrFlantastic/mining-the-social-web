# Social Network Analysis  

According to Wikipedia,

> “Social network analysis (SNA) is the process of investigating social structures through the use of networks and graph theory. It characterizes networked structures in terms of nodes (individual actors, people, or things within the network) and the ties, edges, or links (relationships or interactions) that connect them.”

It has made its way into virtually every field — again, according to Wikipedia:

> “Social network analysis has emerged as a key technique in modern sociology. It has also gained a significant following in anthropology, biology, demography, communication studies, economics, geography, history, information science, organizational studies, political science, public health, social psychology, development studies, sociolinguistics, and computer science and is now commonly available **as a consumer tool.** ”

## Plan for this project
1. Use `tweepy` to scrape Twitter for my follower and (most of) their followers
2. Create a `pandas` DataFrame from all those connections
3. Use `networkx` to extract a network from this data and run some basic network anaysis
4. Visualize the network in Gephi

We will utilize the Twitter REST API to stream and download data chunks.


### Getting Started
We will build a network using my personal Twitter account: @MrFlantastic

First we need to import the Tweepy and pandas package.

    import tweepy
    import pandas as pd

Then we need to enter our Twitter API credentials available in the "Keys and Tokens" portion of our app to get tokens.

    cust_key = 'XXXXXXXXXXXXX'
    consumer_secret = 'XXXXXXXXXXXXX'
    access_token = 'XXXXXXXXXXXXX'
    access_token_secret = 'XXXXXXXXXXXXX'

At this point we'll specify some parameters when we initialize the API. We set `wait_on_rate_limit` and `wait_on_rate_limit_notify` to `True`. There are rate limits when downloading Twitter data, these throttles will respect the set rate limits and wait until the timeout ends before downloading more data.

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

To start the data download, we will get all the followers from my profile. We need to set the ID of this user.

    me = api.get_user(screen_name = 'MrFlantastic')
    me.id

My user ID is:

A network consists of nodes (or vertices) and links (or edges). For this network, we will use individual user accounts as nodes and followers as links. Our goal, therefore, is to create an edge DataFrame of user IDs with two columns: source and target. For each row, the target follows the source. To start, we want to list all of my followers as targets.

The screenshot above shows the structure of the DataFrame we want to create. The first column, the “source”, is my user ID (1210627806) and the second column, the “target”, are all of my followers.

The following code creates a list of my followers.


fin.