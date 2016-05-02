from nltk.sentiment.vader import SentimentIntensityAnalyzer


def estimate_sentiment(text):
	sid = SentimentIntensityAnalyzer()
	# 'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0
	return sid.polarity_scores(text)['neg']


def estimate_for_list(strings):
	return sum(map(estimate_sentiment, strings)) / len(strings)

# if __name__ == '__main__':
	# arr = ['']
	# print estimate_sentiment('')['compound']
	# print estimate_for_list(arr)

