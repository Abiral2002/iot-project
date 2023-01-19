# Code for motor
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
class MotorController:
    def __init__(self) -> None:
        self.isOpen=False
        self.PIN=11
        GPIO.setup(self.PIN,GPIO.OUT)
        self.servo=GPIO.PWM(11,50)
        self.servo.start(0)
        self.servo.ChangeDutyCycle(6.5)
        self.flush=lambda : GPIO.cleanup() 

    def open(self):
        self.isOpen=True
        self.servo.ChangeDutyCycle(2)
        self.servo.start(0)
        return

    def close(self):
        self.isOpen=False
        self.servo.ChangeDutyCycle(6.5)
        self.servo.start(0)
        return