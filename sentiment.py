import sys, tweepy, csv, re
from textblob import TextBlob


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, searchTerm):
        # authenticating
        consumerKey = 'M5N69WvF5voLOTqlpMO10RE5e'
        consumerSecret = 'u8ZDalI3qCAlTCAJ0Fj6ynNC8D9zV43AMexXmpzF5Sz2u1Ne5S'
        accessToken = '1230104751250927616-CVlNYnDRXa76al9W0FPklU5JSBXaZu'
        accessTokenSecret = 'E0IYZsFupOquVAbmRLugEIYJXxFDoSqAeslMViYDqsTAX'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        NoOfTerms = 1000
        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0):
                positive += 1
            elif (analysis.sentiment.polarity < 0):
                negative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms
        po = 0

        # printing out data
        if (polarity == 0):
            po = "Neutral"
        elif (polarity > 0):
            po = "Positive"
        elif (polarity < 0):
            po = "Negative"

        popo = str(positive)
        pong = str(negative)
        ponu = str(neutral)
        return po, popo, pong, ponu

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')