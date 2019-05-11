import numpy as np 
import pandas as pd 
import json
import time
import requests
import signal
import sys
from google.cloud import language
from google.api_core.exceptions import InvalidArgument

class sentiment():

    Z_data = {}
    influencerUsername = ""

    def __init__(self):
        print("in init")

    def GetDPBro(self):
        with open('./'+self.influencerUsername+'/'+self.influencerUsername+'.json', encoding="utf8") as json_file:  
            self.Z_data = json.load(json_file)


    def sentimentTheComments(self):
        data = [['post_id', 'comments']]
        for post in self.Z_data['GraphImages']:
            row = []
            row.append(post['id'])
            comments = post['comments']['data']
            comment_arr = []
            for comment in comments: 
                comment_arr.append(comment['text'])
            row.append(comment_arr)
            data.append(row)
        zoella_posts_df = pd.DataFrame(data, columns=['post_id', 'comments'])
        zoella_posts_df = zoella_posts_df.drop([0])
        client = language.LanguageServiceClient()

        count = 0
        positive_count = 0
        neutral_count = 0
        negative_count = 0

        def detect_sentiment(text):
            """Detects sentiment in the text."""

            document = language.types.Document(
                content=text,
                type=language.enums.Document.Type.PLAIN_TEXT)

            sentiment = client.analyze_sentiment(document).document_sentiment

            return sentiment.score, sentiment.magnitude

        def print_summary():
            print()
            print('Total comments analysed: {}'.format(count))
            print('Positive : {} ({:.2%})'.format(positive_count, positive_count / count))
            print('Negative : {} ({:.2%})'.format(negative_count, negative_count / count))
            print('Neutral  : {} ({:.2%})'.format(neutral_count, neutral_count / count))

        for i, row in zoella_posts_df.iterrows():
            if i == 60: 
                break; 
            comments = row[1][:10]
            for line in comments: 
                # use a try-except block since we occasionally get language not supported errors
                try:
                    score, mag = detect_sentiment(line)
                except InvalidArgument as e:
                    # skip the comment if we get an error
                    print('Skipped 1 comment: ', e.message)
                    continue

                # increment the total count
                count += 1

                # depending on whether the sentiment is positve, negative or neutral, increment the corresponding count
                if score > 0:
                    positive_count += 1
                elif score < 0:
                    negative_count += 1
                else:
                    neutral_count += 1

                # calculate the proportion of comments with each sentiment
                positive_proportion = positive_count / count
                neutral_proportion = neutral_count / count
                negative_proportion = negative_count / count

                print(
                    'Count: {}, Positive: {:.3f}, Neutral: {:.3f}, Negative: {:.3f}'.format(
                        count, positive_proportion, neutral_proportion, negative_proportion))


        print_summary()

LikePredictInstance = LikePredict()
LikePredictInstance.influencerUsername = "zoella"
LikePredictInstance.GetDPBro()
LikePredictInstance.sentimentTheComments()
