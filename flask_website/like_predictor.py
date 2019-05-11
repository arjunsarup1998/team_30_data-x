import numpy as np 
import pandas as pd
import json
import time
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import linear_model



class LikePredict():

    day = 0
    epochEntry = 0
    likeValuePredicted = 0
    influencerUsername = ""
    influencerTopic = ""
    influencerDP = ""
    AB_data = {}

    pos_sentiment = 0.0
    neg_sentiment = 0.0
    neutral_sentiment = 0.0

    def __init__(self):
        print("in init")

    def GetDPBro(self):
        with open('./'+self.influencerUsername+'.json', encoding="utf8") as json_file:  
            self.AB_data = json.load(json_file)

        self.influencerTopic =  'images/'+self.influencerUsername+'.png'
        self.influencerDP = self.AB_data['GraphImages'][0]["display_url"]


    def trainLikePredict(self):

        data = [['DOW', 'day', 'month', 'year', 'time', 'epoch', 'num_likes', 'num_comments']]

        for entry in self.AB_data['GraphImages']: 
            epoch = entry['taken_at_timestamp']
            t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(epoch))
            row = t.split(' ')
            row[0] = row[0][:len(row[0])-1]
            row.append(epoch)
            row.append(entry['edge_media_preview_like']['count'])
            row.append(entry['edge_media_to_comment']['count'])
            #row.append(len(entry['edge_media_to_caption']['edges']['node']['text']))
            data.append(row)

        #print(data)

        AB_df = pd.DataFrame(data, columns=['DOW', 'day', 'month', 'year', 'time', 'epoch', 'num_likes', 'num_comments'])
        AB_df = AB_df.drop([0])

        curr_index = 1
        previous_likes = np.array([])

        previous_likes_for_prediction = AB_df['num_likes'][0:10].mean()         #added this

        while (curr_index <= len(AB_df)):
            end_index = min(len(AB_df), curr_index + 10)
            previous_likes = np.append(previous_likes, AB_df['num_likes'][curr_index:end_index].mean())
            curr_index=curr_index + 1
            
        previous_likes[len(AB_df) - 1] = 0
        AB_df['previous_likes'] = previous_likes

        avg_likes = AB_df['num_likes'].mean()
        AB_df['datetime'] = pd.to_datetime(AB_df['time'])
        AB_df['hour'] = [i.hour for i in AB_df['datetime']]

        AB_df['avg_likes'] = pd.Series(np.ones(1401)*avg_likes)
        AB_df['follower_count'] = pd.Series(np.ones(1401)*30968015)
        days = pd.get_dummies(AB_df['DOW'])

        months = pd.get_dummies(AB_df['month'])

        AB_df = AB_df.merge(days, left_index = True, right_index = True)
        AB_df = AB_df.merge(months, left_index = True, right_index = True)

        AB_df = AB_df.dropna()

        X = AB_df.loc[:, ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'epoch', 'previous_likes']]
        Y = AB_df.loc[:, 'num_likes']
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, shuffle = True, random_state=100)
        LinearRegressionModel = linear_model.LinearRegression() 
        LinearRegressionModel.fit(x_train, y_train)
        #print("Training: ", LinearRegressionModel.score(x_train, y_train))
        #print("Testing: ", LinearRegressionModel.score(x_test, y_test))

        days_predict = [0,0,0,0,0,0,0]
        days_predict[self.day] = 1
        self.likeValuePredicted = int(LinearRegressionModel.predict([[days_predict[0],days_predict[1],days_predict[2],days_predict[3],days_predict[4],days_predict[5],days_predict[6], self.epochEntry, previous_likes_for_prediction ]])[0])