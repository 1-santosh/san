"""
GraphQL schema for extracting results from a website.
"""
# -*- coding: utf-8 -*-
import graphene
import extraction
import requests
import tweepy

## extractor for website url
# Consumer keys and access tokens, used for OAuth
consumer_key = "CcPrtc4qTQ1YbPcxv09NWc0gH"
consumer_secret =  "H34wruZFC49mzaJI3LpG7qV1UIs7jAVdFrj1KiEGEvUkWf2pwn"
access_key = "847618850-7aCokVrqRm3TiMcfdO0r1iEoDT9dbaDVOdpvFKpI"
access_secret = "LWfPi2T1jDknr7oZplKC9rHuezZp48SBcSo6glnefECTO"



def get_all_tweets(user_list):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []
    final_tweets=[]
    for screen_name in user_list:
        # initialize a list to hold all the tweepy Tweets

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print ("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print ("...%s tweets downloaded so far" % (len(alltweets)))

        for tweet in alltweets:
            print (tweet.id_str, tweet.user.screen_name, tweet.created_at, tweet.full_text.encode("utf-8"))

        outtweets = [[tweet.id_str, tweet.user.screen_name, tweet.created_at, tweet.full_text] for
                     tweet in alltweets]
        final_tweets.append(outtweets)


    return final_tweets
## twitter response


## modifying schemas to accommodate different crawling pipelines for websites
class Website(graphene.ObjectType):

    url = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    image = graphene.String()
    feed = graphene.String()
### simialr to type Website{ type Website {"url":String}
## schema creation
## we can create multiple schemas and multiple resolvers according to the ap
class Websites(graphene.ObjectType):
    value = graphene.List (graphene.String)
    outputlist = graphene.List (graphene.String)


class Query(graphene.ObjectType):
    #parses the url from the input string we passed
    ## this is where field website and url is appearing
    # website = graphene.Field(Website, url=graphene.String())
    somefunc = graphene.Field (Websites, args={'value': graphene.List (graphene.String)})
    # print("url is",url)
    # websites = graphene.Field (Websites, url=graphene.String ())
    # print("website",website)
     ## resolve is used for internal logic of graphql


    def resolve_somefunc(self, info, value):
        extracted = get_all_tweets (value)
        print(extracted)
        ## return field for graphql query
        ## json s3 dumps
        print("value for twitter url is",value)
        return Websites(value=value,
                        outputlist=extracted
                        )

schema = graphene.Schema(query=Query)
### execute schema acts as graphql query