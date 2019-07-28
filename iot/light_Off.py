import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(36,GPIO.OUT)
GPIO.output(36,GPIO.HIGH)
#GPIO.cleanup()
