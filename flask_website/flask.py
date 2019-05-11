from flask import Flask, render_template, flash, redirect, url_for
from index_page_form import InstagramHandleHome, InstagramHandleFormGeneric
from like_predictor import LikePredict
import datetime
app = Flask(__name__)

count = 1

LikePredictInstance = LikePredict()

app.config['SECRET_KEY']='lol'

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def home():
	form = InstagramHandleHome()
	if form.validate_on_submit():
		LikePredictInstance.influencerUsername = form.handle.data
		LikePredictInstance.GetDPBro()
		return redirect(url_for('generic'))
	return render_template('index.html', form = form)

#choose Influencer page
@app.route("/choose")
def choose():
	return render_template('choose.html')

@app.route("/choose2")
def choose2():
	return render_template('choose2.html')


#page with all elements
@app.route("/elements")
def elements():
	return render_template('elements.html')


#form
@app.route("/generic", methods=['GET', 'POST'])
def generic():
	form2 = InstagramHandleFormGeneric()
	if form2.validate_on_submit():
		dateArr=str(form2.dt.data).split("-")
		TimeArr=str(form2.tt.data).split(":")
		LikePredictInstance.epochEntry = datetime.datetime(int(dateArr[0]),int(dateArr[1]),int(dateArr[2]),int(TimeArr[0]),int(TimeArr[1]),int(TimeArr[2])).timestamp()
		LikePredictInstance.day = form2.dt.data.weekday()
		LikePredictInstance.trainLikePredict()
		return redirect(url_for('person'))
	return render_template('generic.html', form = form2)

#final page with al the data
@app.route("/person", methods=['GET', 'POST'])
def person():
	return render_template('person.html',  influencer_name=LikePredictInstance.influencerUsername, influencer_dp = LikePredictInstance.influencerDP, predlikes = LikePredictInstance.likeValuePredicted, photosrc = LikePredictInstance.influencerTopic, posfin = LikePredictInstance.pos_sentiment, negfin = LikePredictInstance.neg_sentiment, neutfin = LikePredictInstance.neutral_sentiment)


if __name__ == '__main__' :
	app.run(debug = True)
