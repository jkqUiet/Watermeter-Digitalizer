import RPi.GPIO as GPIO
import json

with open('config.json') as f:
    config = json.load(f)

GPIO.setmode(GPIO.BCM)

led_pin = config['ledOn']['ledPin']
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin,GPIO.HIGH)

