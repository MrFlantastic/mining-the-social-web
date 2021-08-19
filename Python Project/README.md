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

First we need to import the `tweepy` and `pandas` package.

    import tweepy
    import pandas as pd


## EDIT
Then we need to enter our Twitter API credentials available in the "Keys and Tokens" portion of our app to get tokens.

    cust_key = 'XXXXXXXXXXXXX'
    consumer_secret = 'XXXXXXXXXXXXX'
    access_token = 'XXXXXXXXXXXXX'
    access_token_secret = 'XXXXXXXXXXXXX'


## EDIT
At this point we'll specify some parameters when we initialize the API. We set `wait_on_rate_limit` and `wait_on_rate_limit_notify` to `True`. There are rate limits when downloading Twitter data, these throttles will respect the set rate limits and wait until the timeout ends before downloading more data.

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

To start the data download, we will get all the followers from my profile. We need to set the ID of this user.

    me = api.get_user(screen_name = 'MrFlantastic')
    me.id

My user ID is: 486977981

A network consists of nodes (or vertices) and links (or edges). For this network, we will use individual user accounts as nodes and followers as links. Our goal, therefore, is to create an edge DataFrame of user IDs with two columns: source and target. For each row, the target follows the source. To start, we want to list all of my followers as targets.

Let's discuss the structure of the DataFrame we want to create. The first column, the “source”, is my user ID (486977981) and the second column, the “target”, are all of my followers.

The following code creates a list of my 780 followers.
    
    user_list = ["486977981"]
    follower_list = []
    for user in user_list:
        followers = []
        try:
            for page in tweepy.Cursor(api.followers_ids, user_id=user).pages():
                followers.extend(page)
                print(len(followers))
        except tweepy.TweepError:
            print("error")
            continue
        follower_list.append(followers)

Now that we have a list of all the followers we can put them into a DataFrame.

    df = pd.DataFrame(columns=['source','target']) #Empty DataFrame
    df['target'] = follower_list[0] #Set the list of followers as the target column
    df['source'] = 486977981 #Set my user ID as the source 

This is not a very interesting network. To visualize this simple network, we can use the `NeworkX` package to convert the DataFrame into a graph or network.

    import networkx as nx
    G = nx.from_pandas_edgelist(df, 'source', 'target') #Turn df into graph
    pos = nx.spring_layout(G) #specify layout for visual

Then we plot the graph using `matplotlib`.

    import matplotlib.pyplot as plt
    f, ax = plt.subplots(figsize=(10, 10))
    plt.style.use('ggplot')
    nodes = nx.draw_networkx_nodes(G, pos,
                                   alpha=0.8)
    nodes.set_edgecolor('k')
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.2)

The code above renders a clustered visual - not very interesting. What we really want is to get all the followers of these 780 users. To do this, we will loop through the list of all those 780 users, get their followers, and add those links to the original DataFrame. This is where our code will take a very long time to run because of rate limits.

    user_list = list(df['target']) #Use the list of followers we extracted in the code above i.e. my 450 followers
    for userID in user_list:
        print(userID)
        followers = []
        follower_list = []
    
        # fetching the user
        user = api.get_user(userID)
    
       # fetching the followers_count
        followers_count = user.followers_count
    
        try:
            for page in tweepy.Cursor(api.followers_ids, user_id=userID).pages():
                followers.extend(page)
                print(len(followers))
                if followers_count >= 5000: #Only take first 5000 followers
                    break
        except tweepy.TweepError:
            print("error")
            continue
        follower_list.append(followers)
        temp = pd.DataFrame(columns=['source', 'target'])
        temp['target'] = follower_list[0]
        temp['source'] = userID
        df = df.append(temp)
        df.to_csv("networkOfFollowers.csv")

This code is very similar to the code above in that it gets all the followers of a given user ID. The major difference is that instead of feeding in just one account, we are looping through all 780 accounts that follow me.

Another difference is that if an account has more than 5000 followers, we only take the first 5000 followers. This is because of the way the API works. Each API request will only return 5000 accounts. So if we want all followers from an account that has, say, one million followers, we would need to make 200 individuals requests.
Because of the rate limits, I left this running overnight to get all the data. It makes 15 API requests, then has to wait for 15 minutes, then makes another 15 requests, and so on. So it can take a long time.
Once this is done running, you should have a csv with all of the edges of the network. 

I wrote this all to a csv just so that if it breaks while running I still have all the edges already scraped.
Now read the csv and turn the df into a graph using NetworkX.

    df = pd.read_csv(“networkOfFollowers.csv”) #Read into a df
    G = nx.from_pandas_edgelist(df, 'source', 'target')
Once the data has been converted to a graph, we can run some basic network analytics.
  
    G.number_of_nodes() #Find the total number of nodes in this graph

There are XXX nodes in my network!

##Influence

We can also find the most influential nodes in the network using centrality measures. The most simple measure of centrality is Degree Centrality, which is just a function of the number of connections each node has. The following code finds the number of connections each node has i.e. the degree of each node and sorts them in descending order.
    
    G_sorted = pd.DataFrame(sorted(G.degree, key=lambda x: x[1], reverse=True))
    G_sorted.columns = [‘nconst’,’degree’]
    G_sorted.head()

The node in my network with the highest degree is node XXXXXXXX or @ TheSolarCo. TheSolarCo has a degree of 5039. 5000 of these connections are the 5000 followers of this node that we scraped. But this means there are 39 additional connections — meaning TheSolarCo follows 39 accounts that follow me.

To get the username of an account given the user ID use the following code, similar to how we got our user ID above.

    u = api.get_user(XXXXXX)
    u.screen_name

Because the network is so big now (over XXXXX nodes), any analytics will take a long time to run and any visualization will be a complete mess. For the rest of this tutorial, we will filter the network down to a more manageable number of nodes. We do this using the `k_core` function of `NetworkX`. The `k_core` function filters out nodes with degree less than a given number, k.

In this example, I set k equal to 10, which reduces the number of nodes in the graph to about 1000.

    G_tmp = nx.k_core(G, 10) #Exclude nodes with degree less than 10

With this smaller graph we can easily do some network analytics. We start by splitting the graph into groups using a `community` detection algorithm.

    from community import community_louvain
    partition = community_louvain.best_partition(G_tmp)
    #Turn partition into dataframe
    partition1 = pd.DataFrame([partition]).T
    partition1 = partition1.reset_index()
    partition1.columns = ['names','group']

We need to run the degree centrality code again now that our network is smaller.
    
    G_sorted = pd.DataFrame(sorted(G_tmp.degree, key=lambda x: x[1], reverse=True))
    G_sorted.columns = ['names','degree']
    G_sorted.head()
    dc = G_sorted

Now that we have the nodes split into groups and the degree of each node, we combine these into one DataFrame.

    combined = pd.merge(dc,partition1, how='left', left_on="names",right_on="names")

Now we can visualize this graph using the following code.

    pos = nx.spring_layout(G_tmp)
    f, ax = plt.subplots(figsize=(10, 10))
    plt.style.use('ggplot')
    #cc = nx.betweenness_centrality(G2)
    nodes = nx.draw_networkx_nodes(G_tmp, pos,
                                    cmap=plt.cm.Set1,
                                    node_color=combined['group'],
                                    alpha=0.8)
    nodes.set_edgecolor('k')
    nx.draw_networkx_labels(G_tmp, pos, font_size=8)
    nx.draw_networkx_edges(G_tmp, pos, width=1.0, alpha=0.2)
    plt.savefig('twitterFollowers.png')

What a mess. I’m sure there are ways to make that visual look better using matplotlib, but at this point, I'll export the file to csv format and use Gephi to visualize.

    combined = combined.rename(columns={"names": "Id"}) #I've found Gephi really likes when your node column is called 'Id'
    edges = nx.to_pandas_edgelist(G_tmp)
    nodes = combined['Id']
    
    edges.to_csv("edges.csv")
    combined.to_csv("nodes.csv")

fin.
