# Code for motor
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
class MotorController:
    def __init__(self) -> None:
        self.isOpen=False
        self.OPEN=5
        self.CLOSE=7

    def open(self):
        self.isOpen=True
        GPIO.setout(self.OPEN,GPIO.OUT)
        GPIO.output(self.OPEN,True)
        sleep(2)
        GPIO.output(self.OPEN,False)
        pass

    def close(self):
        self.isOpen=False
        GPIO.setout(self.CLOSE,GPIO.OUT)
        GPIO.output(self.CLOSE,True)
        sleep(2)
        GPIO.output(self.CLOSE,False)
        pass