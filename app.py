import pandas as pd
import re
from textblob import TextBlob
from flask import Flask, render_template , redirect, url_for, request
from flask import jsonify
app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("start.html")


@app.route('/get_started')
def get_started():
    return render_template("index.html")

@app.route('/home1')
def home1():
    return render_template("start.html")

@app.route('/developer')
def developer():
    return render_template("developer.html")

@app.route('/new_tweet_page')
def new_tweet_page():
    return render_template("index.html")

#@app.route("/predict", methods=['POST','GET'])
@app.route("/predict", methods=['POST'])
def pred():
    if request.method == 'POST':
        query = request.form['query']

        positive = negative = neutral = 0

        # Iterate through the tweets in the dataset
        for tweet in df['text']:
            # Check if the search word/phrase is in the tweet
            if query.lower() in tweet.lower():
                blob = TextBlob(tweet)
                sentiment = blob.sentiment
                polarity = sentiment.polarity

                # Determine sentiment based on the compound score
                if polarity > 0:
                    positive += 1
                elif polarity < 0:
                    negative += 1
                else:
                    neutral += 1

        res = {
            'Positive Tweets': positive,
            'Negative Tweets': negative,
            'Neutral Tweets': neutral
        }

        return render_template('result.html', result=res)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    query = request.args.get('query')
    print(query)
    return render_template('result.html', query=query)


if __name__ == '__main__': 

    # Load your dataset into a pandas DataFrame
    df = pd.read_csv('Twitter_Data.csv')
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    app.debug=True
    app.run(host='localhost')

