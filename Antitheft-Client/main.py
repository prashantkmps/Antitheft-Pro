import os
import time
import threading

import RPi.GPIO as GPIO
import multiprocessing

import cv2
import numpy as np

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import signal

EMAIL = 'proantitheft@gmail.com'
PASSWORD = 'sciencesciences8307'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
enablesystem=True


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

# Functions

class TimeoutException(Exception):   # Custom exception class
    pass


def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException


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


def gpio_high(pinno):
    pinno=int(pinno)
    print('high=', pinno)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinno, GPIO.OUT)
    GPIO.output(pinno, GPIO.HIGH)


def gpio_low(pinno):
    pinno=int(pinno)
    print('low=',pinno)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinno, GPIO.OUT)
    GPIO.output(pinno, GPIO.LOW)


def mail_to_owners():
    print('mail_to_owners')
    # import socket
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # print(s.getsockname()[0])
    # x = s.getsockname()[0]
    # s.close()

    # fromaddr = EMAIL
    # toaddr = "prateekagrawal89760@gmail.com"
    # msg = MIMEMultipart()
    # msg['From'] = fromaddr
    # msg['To'] = toaddr
    # msg['Subject'] = "Motion Detected"
    # body = msg.attach(MIMEText('hello motion detected', 'plain'))

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login(fromaddr, PASSWORD)
    # text = msg.as_string()
    # server.sendmail(fromaddr, toaddr, text)
    # server.quit()


def call_to_owners():

    print('called')
    # # Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
    # # and use the E.164 format, for example: "+12025551234"
    # TWILIO_PHONE_NUMBER = "+17738255252"

    # # list of one or more phone numbers to dial, in "+19732644210" format
    # numbers_list = ["+917464847884", "+919458412853", ]

    # # URL location of TwiML instructions for how to handle the phone call
    # TWIML_INSTRUCTIONS_URL = \
    #     "http://static.fullstackpython.com/phone-calls-python.xml"

    # # replace the placeholder values with your Account SID and Auth Token
    # # found on the Twilio Console: https://www.twilio.com/console
    # client = TwilioRestClient("AC2bb615af88faf946ecb4d1e3c013771e", "74cf75c65a2a39660f6401fbc58aa563")

    # """Dials one or more phone numbers from a Twilio phone number."""
    # for number in numbers_list:
    #     print("Dialing " + number)
    #     # set the method to "GET" from default POST because Amazon S3 only
    #     # serves GET requests on files. Typically POST would be used for apps
    #     client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER, url=TWIML_INSTRUCTIONS_URL, method="GET")


def sms_to_owners():

    print('sms')
    # Your Account Sid and Auth Token from twilio.com/console
    # account_sid = 'AC2bb615af88faf946ecb4d1e3c013771e'
    # auth_token = '74cf75c65a2a39660f6401fbc58aa563'
    # client = TwilioRestClient("AC2bb615af88faf946ecb4d1e3c013771e", "74cf75c65a2a39660f6401fbc58aa563")

    # message = client.messages.create(
    #     body='Hiii, your belonging is in danger !',
    #     from_='+17738255252',
    #     to='+917464847884'
    # )

    # print(message.sid)

def verifyface():
    recognizer = cv2.createLBPHFaceRecognizer()
    recognizer.load('recognizer/trainingData.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    found = False
    cam = cv2.VideoCapture(0)
    font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                if (Id == 101):
                    Id = "PRATEEK"
                    found = True
                    print(Id)
                    break
                elif (Id == 456):
                    Id = "PRASHANT"
                    found = True
                    print(Id)
                    break
            else:
                Id = "Unknown"
            cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
        if found:
            break
        #cv2.imshow('im',im)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    if found:
        cam.release()
        cv2.destroyAllWindows()
        return True
    else:
        return False


while True:
    print("Run recurring task")
    if enablesystem:
        if detectmotion():
            gpio_high(pinno=bulbpin)
            verified=False
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)
            try:
                verified = verifyface()
            except TimeoutException:
                pass
            else:
                signal.alarm(0)
            if not verified:
                gpio_high(pinno=sirenpin)
                gpio_high(pinno=gaspin)
                gpio_high(pinno=doorpin)
                mail_to_owners()
                call_to_owners()
                sms_to_owners()
                while True:
                    if not enablesystem:
                        gpio_low(pinno=sirenpin)
                        gpio_low(pinno=gaspin)
                        gpio_low(pinno=doorpin)
                        break
                    time.sleep(0.1)
            else:
                gpio_low(pinno=bulbpin)
    time.sleep(1)
