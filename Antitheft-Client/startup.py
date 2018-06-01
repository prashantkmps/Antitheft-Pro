#!/usr/bin/env python

import RPi.GPIO as GPIO


pinno=23
pinno1=24

GPIO.setmode(GPIO.BCM)

GPIO.setup(pinno1, GPIO.OUT)

GPIO.output(pinno1, GPIO.LOW)
GPIO.setup(pinno, GPIO.OUT)

GPIO.output(pinno, GPIO.LOW)
