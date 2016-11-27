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

hasMail = False

mail = Mail(app)

UPLOAD_FOLDER = '/'

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
    return redirect('http://mailsnail.tech/api/notify')

# def newtonian_temperature_model():
#T_0 = 76.66 #centigrade
#T_a = 40 #centigrade
#t = np.array(range(1,180,10), dtype=np.uint8)
#k = np.ones(len(t), dtype=np.uint8)*0.01 #per minute
#T_now = T_a + (T_0 - T_a)*np.e**(-k*t)
#if T_now > 45: #has to be maximum 45 centigrade to drink
#    return "I'm too hot to drink!"
#if T_now < 45:
#    return "Drink me I'm cool!"



@app.route("/api/notify")
# def get_message_list():
#     TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
#     TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

#     client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     messagelist = client.messages.list()
#     return messagelist

def send_notification():
    #if request.method == 'POST':
        # file = request.files['file']
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file',filename=filename))
    hasMail = True
    msg = Message('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),sender="noreply.mailsnail@gmail.com",bcc=['jeanpaul.breuer@gmail.com'])
    msg.body = "You have received mail in your physical mailbox! Timestamp: {:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
    msg.html = "<b>You have received mail in your physical mailbox!</b>"
    mail.send(msg)

    today = datetime.date.today()
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])
    api.PostUpdate('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    return "You got mail!"
    #return "You got mail!"

#def send_sms():
#    resp = twilio.twiml.Response()
#    resp.message('MailSnail has arrived! Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
#    return str(resp)

#def tweet():


@app.route("/api/subscribe/new", methods=['GET', 'POST'])
# def get_messages_list():
#     TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
#     TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

#     client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     messagelist = client.messages.list()
#     return messagelist

def send_subscribed_email():
    msg = Message('Thanks for subscribing to our email notification service!',
    sender="noreply.mailsnail@gmail.com",
    bcc=['jeanpaul.breuer@gmail.com'])

    msg.body = "Thanks for subscribing to our email notification service!"
    msg.html = "<b>Thanks for subscribing to our email notification service!</b>"
    mail.send(msg)

    resp = twilio.twiml.Response()
    resp.message('Thanks for subscribing to our email notification service!')
    return str(resp)

@app.route("/api/mail/has")
def has_new_mail():
    if (hasMail):
        hasMail = False;
        return 1;
    else:
        return 0;

if __name__ == "__main__":
    app.run(host='localhost')
