from flask import Flask
import twitter

app = Flask(__name__)

@app.route('/')
def tweet():
    api = twitter.Api(consumer_key='1fxSq5Wq32O26y1rEH5r34oEF',
        consumer_secret='zyD0yGM3S0GEGQs1hQPlFsDBXwYnV8mzXU8NJQduWXNnf41FFY',
        access_token_key='4921300870-DNtLkcmctArX59cOylr1RWSqVVeU2s3jqWdWk3p',
        access_token_secret='040XjcvMNkwDHw4s3fi5MclGHQq6PtF7DjBswxLoJhQtM')
    return api.PostUpdate('You have mail!')

