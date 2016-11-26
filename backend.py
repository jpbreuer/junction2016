from flask import Flask
import os
import twitter

app = Flask(__name__)

@app.route('/')
def tweet():
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret="TWITTER_ACCESS_TOKEN_SECRET")
    return api.PostUpdate('You have mail!')

#@app.route('/')