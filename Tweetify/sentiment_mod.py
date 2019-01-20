import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt

class TwitterClient(object):
	def __init__(self):
		consumer_key = '9xhDXeOzwsZ0dpuzV2q76yzSE'
		consumer_secret = 'lxdQ3rtVKEHEMDiflBETQWqXKHRYJj3gQeS28NCHKx2V8zzx8R'
		access_token = '1082249754472374272-C8CWU3h6zNZrTjavuw6bRBUZiE7buU'
		access_token_secret = '5iKhHg7cCZ7r3N3n3f2wesQY0VYwSJ86BD4Erck1WTJAU'

		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+://\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def plotPieChart(positive, negative, neutral, output, query,count):
	labels = ['Positive [' + str(positive) + '%]','Negative [' + str(negative) + '%]', 'Neutral [' + str(neutral) + '%]']
	sizes = [positive,negative, neutral]
	colors = ['darkgreen', 'red', 'gold']
	patches,text = plt.pie(sizes,colors=colors, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.title('How people are reacting on ' + query + ' by analyzing ' + str(count) + ' Tweets and Output is :' + str(output) + '.' )
	plt.axis('equal')
	plt.tight_layout()
	plt.show()



def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	# calling function to get tweets
	print("Enter the query")
	query=input()
	print("Enter total number of tweets to be analysed")
	count=int(input())
	tweets = api.get_tweets(query , count)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	pres= 100*len(ptweets)/len(tweets)
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	nres=100*len(ntweets)/len(tweets)
	print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
	neures=100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
	if (pres > nres and pres > neures):
		output="Positive"
	elif (nres > pres and nres > neures):
		output = "Negative"
	else:
		output = "Neutral"
	plotPieChart(pres, nres, neures, output, query, count)


# printing first 5 positive tweets
	#print("\n\nPositive tweets:")
	#for tweet in ptweets[:10]:
	#	print(tweet['text'])

	# printing first 5 negative tweets
	#print("\n\nNegative tweets:")
	#for tweet in ntweets[:10]:
	#	print(tweet['text'])


if __name__ == "__main__":
	# calling main function
	main()
