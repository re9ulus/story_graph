from nltk.sentiment.vader import SentimentIntensityAnalyzer


def estimate_sentiment(text):
	sid = SentimentIntensityAnalyzer()
	return sid.polarity_scores(text)['pos'], sid.polarity_scores(text)['neg']


def estimate_for_list(strings):
	sentiment = sorted(map(estimate_sentiment, strings))
	pos, neg = [], []
	for p, n in sentiment:
		if p:
			pos.append(p)
		if n:
			neg.append(n)

	pos, neg = sum(pos) / (len(sentiment) + 1), sum(neg) / (len(sentiment) + 1) # len(pos) + 1, len(neg)

	return (pos - neg) * 100

# if __name__ == '__main__':
	# arr = ['']
	# print estimate_sentiment('')['compound']
	# print estimate_for_list(arr)

