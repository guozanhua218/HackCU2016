#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import codecs
import csv
import json
from keys import *


def get_all_tweets(topic): #could also be a user ID for user's tweets.
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	alltweets = []	
	if api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']==0:
		auth = tweepy.OAuthHandler(consumer_key2, consumer_secret2)
		auth.set_access_token(access_key2, access_secret2)
		api = tweepy.API(auth)
	if api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']==0:
		auth = tweepy.OAuthHandler(consumer_key3, consumer_secret3)
		auth.set_access_token(access_key3, access_secret3)
		api = tweepy.API(auth)
	#initialize a list to hold all the tweepy Tweets
	#ahmed was here
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.search(q=topic, rpp=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	# #keep grabbing tweets until there are no tweets left to grab
	# while len(new_tweets) > 0:
	# 	#all subsiquent requests use the max_id param to prevent duplicates
	# 	new_tweets = api.search(q=topic, rpp=200)	
		
	# 	#save most recent tweets
	# 	alltweets.extend(new_tweets)
		
	# 	#update the id of the oldest tweet less one
	# 	oldest = alltweets[-1].id - 1
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.text.encode("utf-8"), tweet.id_str, tweet.author._json['screen_name'], tweet.created_at, 'false'] for tweet in alltweets]
	return outtweets

def get_user_tweets(screen_name): #could also be a user ID for user's tweets.
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key2, consumer_secret2)
	auth.set_access_token(access_key2, access_secret2)
	api = tweepy.API(auth)

	alltweets = []	
	if api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']==0:
		auth = tweepy.OAuthHandler(consumer_key2, consumer_secret2)
		auth.set_access_token(access_key2, access_secret2)
		api = tweepy.API(auth2)
	#initialize a list to hold all the tweepy Tweets
	#ahmed was here
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	# #keep grabbing tweets until there are no tweets left to grab
	# while len(new_tweets) > 0:
	# 	#all subsiquent requests use the max_id param to prevent duplicates
	# 	new_tweets = api.search(q=topic, rpp=200)	
		
	# 	#save most recent tweets
	# 	alltweets.extend(new_tweets)
		
	# 	#update the id of the oldest tweet less one
	# 	oldest = alltweets[-1].id - 1
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.text.encode("utf-8"), tweet.id, screen_name, tweet.created_at, "true"] for tweet in alltweets]
	return outtweets

def trending_topics():
	topics = []
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	#2367231
	loc = api.trends_closest(40.014828, -105.258176)[0]
	trends = api.trends_place(id=loc['woeid'])[0]
	for i in trends['trends']:
		topics.append(i['name'].encode('utf-8'))
	return topics