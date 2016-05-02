from nltk.sentiment.vader import SentimentIntensityAnalyzer


def estimate_sentiment(text):
	sid = SentimentIntensityAnalyzer()
	return sid.polarity_scores(text)


if __name__ == '__main__':
	print estimate_sentiment('fuck yourself in the ass')['compound']
	print estimate_sentiment('suck my dick')
	print estimate_sentiment('i love you')
