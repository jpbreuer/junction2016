import config

from flask import Flask, request, redirect
from flask_mail import Mail, Message

from tesserwrap import Tesseract
from PIL import Image, ImageEnhance, ImageFilter

import os
import numpy as np

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

@app.route('/api/processing')
def parse_img():
    im = Image.open("./temp.jpg") # the second one
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('./temp2.jpg')
    tr = Tesseract(os.environ["TESSDATA_PREFIX"],"eng")
    text = tr.ocr_image(Image.open('./temp2.jpg'))
    return text

def newtonian_temperature_model():
    T_0 = 76.66 #centigrade
    k = 0.054 #per minute
    T_a = 23 #centigrade
    t = range(1,1000,4)
    #has to be maximum 45 centigrade to drink
    T_now = T_a + (T_0 + T_a)*np.e**(-k*t)
    if T_now > 45:
        return "I'm too hot to drink!"
    if T_now < 45:
        return "Drink me I'm cool!"


@app.route("/api/notify")
def get_message_list():
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
 
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    messagelist = client.messages.list()
    return messagelist

def send_email():
    msg = Message('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
                  sender="noreply.mailsnail@gmail.com",
                  bcc=get_message_list())
    msg.body = "You have received mail in your physical mailbox! Timestamp: {:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
    msg.html = "<b>You have received mail in your physical mailbox!</b>"
    mail.send(msg)

def send_sms():
    resp = twilio.twiml.Response()
    resp.message('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    return str(resp)

def tweet():
    today = datetime.date.today()
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])
    return api.PostUpdate('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))


@app.route("/api/subscribe/new", methods=['GET', 'POST'])
def get_messages_list():
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
 
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    messagelist = client.messages.list()
    return messagelist

def send_subscribed_sms():
    resp = twilio.twiml.Response()
    resp.message('Thanks for subscribing to our email notification service!')
    return str(resp)

def send_subscribed_email():
    msg = Message('Thanks for subscribing to our email notification service!',sender="noreply.mailsnail@gmail.com",bcc=get_messages_list())
    msg.body = "Thanks for subscribing to our email notification service!"
    msg.html = "<b>Thanks for subscribing to our email notification service!</b>"
    mail.send(msg)

if __name__ == "__main__":
    app.run(host='localhost')