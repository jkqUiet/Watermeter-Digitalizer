import RPi.GPIO as GPIO
import json

with open('config.json') as f:
    config = json.load(f)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin = config['ledOff']['ledPin']
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin,GPIO.LOW)
GPIO.cleanup()
