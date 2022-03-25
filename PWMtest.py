import RPi.GPIO as GPIO
import time
import sys

PWMLed = 18
PWMpel = 12
PWMvarme = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMLed,GPIO.OUT)
GPIO.setup(PWMpel,GPIO.OUT)
GPIO.setup(PWMvarme,GPIO.OUT)
GPIO.setwarnings(False)
pi_pwm = GPIO.PWM(PWMLed,1000)		#create PWM instance with frequency
peltier = GPIO.PWM(PWMpel, 1000)
varme = GPIO.PWM(PWMvarme, 1000)
pi_pwm.start(0)
peltier.start(0)
varme.start(0)

def pwm():
    while True:
        pi_pwm.ChangeDutyCycle(0)
        peltier.ChangeDutyCycle(0)
        varme.ChangeDutyCycle(70)

while True:
    try:
        pwm()

    except KeyboardInterrupt:
        pi_pwm.stop()
        GPIO.cleanup()
        sys.exit()