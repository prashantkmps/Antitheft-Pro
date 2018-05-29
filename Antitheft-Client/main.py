import os
import time
import threading
from flask import *
import RPi.GPIO as GPIO
import multiprocessing
from twilio.rest import TwilioRestClient

app = Flask(__name__)

# ################ Connection Setup ####################

# bulb = pin 16 ( GPIO 23 )
# siren = pin 18 ( GPIO 24 )
# pir = pin 22 ( GPIO 25 )
# ServoMotor ( Gas ) = pin 32 ( GPIO 12 )
# DistanceSensor = pin 38 ( GPIO 10 ), pin 39 ( GPIO 20 )
# ServoMotor ( door ) = pin 7 ( GPIO 4 )

bulbpin = 23
sirenpin = 24
pirpin = 25
gaspin = 12
doorpin = 4

# ################ End  Connection Setup ####################


# ################ Response Codes ####################

SUCCESS = 'success'
UNSUCCESS = 'unsuccess'
YES = 'yes'
NO = 'no'


# ################ End  Response codes ####################

# Functions

def detectmotion():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pirpin, GPIO.IN)

    try:
        time.sleep(0.1)  # to stabilize sensor
        while True:
            if GPIO.input(pirpin):
                print("Motion Detected...")
                return True
            else:
                print('no')
            time.sleep(0.1)  # loop delay, should be less than detection delay

    except:
        GPIO.cleanup()


def bulb(high_or_low):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bulbpin, GPIO.OUT)
    GPIO.output(bulbpin, high_or_low)


def siren(high_or_low):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sirenpin, GPIO.OUT)
    GPIO.output(sirenpin, high_or_low)


def gas(high_or_low):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gaspin, GPIO.OUT)
    GPIO.output(gaspin, high_or_low)


def door(high_or_low):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(doorpin, GPIO.OUT)
    GPIO.output(doorpin, high_or_low)


def mail_to_owners():

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    x = s.getsockname()[0]
    s.close()

    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText

    fromaddr = EMAIL
    toaddr = "prateekagrawal89760@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Motion Detected"
    body = msg.attach(MIMEText('hello motion detected', 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, PASSWORD)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def call_to_owners():
	
	# Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
	# and use the E.164 format, for example: "+12025551234"
	TWILIO_PHONE_NUMBER = "+17738255252"

	# list of one or more phone numbers to dial, in "+19732644210" format
	numbers_list = ["+917464847884", "+919458412853",]

	# URL location of TwiML instructions for how to handle the phone call
	TWIML_INSTRUCTIONS_URL = \
	  "http://static.fullstackpython.com/phone-calls-python.xml"

	# replace the placeholder values with your Account SID and Auth Token
	# found on the Twilio Console: https://www.twilio.com/console
	client = TwilioRestClient("AC2bb615af88faf946ecb4d1e3c013771e", "74cf75c65a2a39660f6401fbc58aa563")


	"""Dials one or more phone numbers from a Twilio phone number."""
	for number in numbers_list:
	    print("Dialing " + number)
	# set the method to "GET" from default POST because Amazon S3 only
	# serves GET requests on files. Typically POST would be used for apps
	    client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")


def sms_to_owners():
	# Your Account Sid and Auth Token from twilio.com/console
	account_sid = 'AC2bb615af88faf946ecb4d1e3c013771e'
	auth_token = '74cf75c65a2a39660f6401fbc58aa563'
	client = TwilioRestClient("AC2bb615af88faf946ecb4d1e3c013771e", "74cf75c65a2a39660f6401fbc58aa563")


	message = client.messages.create(
		                      body='Hiii, your belonging is in danger !',
		                      from_='+17738255252',
		                      to='+917464847884'
		                  )

	print(message.sid)


@app.route('/isenablesystem')
def isenablethesystem():
    if app.secret_key == request.args.get('secretkey'):
        if app.config['enablesystem']:
            resp = make_response(YES)
        else:
            resp = make_response(NO)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/enablesystem')
def enablethesystem():
    if app.secret_key == request.args.get('secretkey'):
        app.config['enablesystem'] = True
        resp = make_response(SUCCESS)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/disablesystem')
def disablethesystem():
    if app.secret_key == request.args.get('secretkey'):
        app.config['enablesystem'] = False
        resp = make_response(SUCCESS)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("Run recurring task")
            if app.config['enablesystem']:
                if detectmotion():
                    bulb(True)
                    if not verifyface(30):
                        siren(True)
                        mail_to_owners()
                        call_to_owners()
                        sms_to_owners()
                        gas(True)
                        door(True)
                        while True:
                            if not app.config['enablesystem']:
                                siren(False)
                                gas(False)
                                door(False)
                                break
                            time.sleep(0.1)
                    else:
                        bulb(False)
            time.sleep(1)

    threading.Thread(target=run_job).start()


if __name__ == '__main__':
    EMAIL = 'proantitheft@gmail.com'
    PASSWORD = 'sciencesciences8307'
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    app.secret_key = 'VA7e5qS/5SSS5~8DF!kKK{KN5/.@4T'
    app.config['BASE_DIR'] = BASE_DIR
    app.config['enablesystem'] = True
    app.run('0.0.0.0', 3000, True)
