import config

from flask import Flask, request, redirect
from flask_mail import Mail, Message

from tesserwrap import Tesseract
from PIL import Image, ImageEnhance, ImageFilter

import os

import twitter
import datetime

import twilio.twiml
from twilio.rest import TwilioRestClient


app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'noreply.mailsnail@gmail.com',
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"],
))

mail = Mail(app)

@app.route('/test')
def tweet():
    today = datetime.date.today()
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])
    return api.PostUpdate('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

@app.route('/')
def parse_img():
    im = Image.open("./temp.jpg") # the second one
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('./temp2.jpg')
    tr = Tesseract(os.environ["TESSDATA_PREFIX"],"eng")
    text = tr.ocr_image(Image.open('./temp1.jpg'))
    return text


@app.route("/test")
def send_message():
    msg = Message('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
                  sender="noreply.mailsnail@gmail.com",
                  bcc=["jeanpaul.breuer@gmail.com"])#matt@mbell.me","jeanpaul.breuer@gmail.com","wil.klopp@gmail.com","noreply.mailsnail@gmail.com"])
    msg.body = "You have received mail in your physical mailbox!"
    msg.html = "<b>You have received mail in your physical mailbox!</b>"
    mail.send(msg)

@app.route("/api/subscribe/new", methods=['GET', 'POST'])
def get_message_list():
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
 
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    messagelist = client.messages.list()
    return messagelist

def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    resp = twilio.twiml.Response()
    resp.message('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    return str(resp)


if __name__ == "__main__":
    app.run(host='http://mailsnail.tech/')