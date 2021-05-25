import RPi.GPIO as GPIO
from time import sleep

#Motor A
enA = 25
in1 = 23
in2 = 24
#Motor B
enB = 22
in3 = 17
in4 = 27
#Setup as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(enA, GPIO.HIGH)
GPIO.output(enB, GPIO.HIGH)
#Enable variable speeds through pwm
pA = GPIO.PWM(enA, 1000)
pB = GPIO.PWM(enB, 1000)
pA.start(25)
pB.start(25)
speeds = [25, 50, 75]

#Cycle through testing forward and backward at different speeds
for values in speeds:
    pA.ChangeDutyCycle(values)
    pB.ChangeDutyCycle(values)

    #forward
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(enB, GPIO.HIGH)
    sleep(3)

    #stop
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(enA, GPIO.LOW)
    GPIO.output(enB, GPIO.LOW)
    sleep(3)

    #backward
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(enB, GPIO.HIGH)
    sleep(3)

    #stop
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(enA, GPIO.LOW)
    GPIO.output(enB, GPIO.LOW)
    sleep(3)

GPIO.cleanup()
