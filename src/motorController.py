# Code for motor
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
class MotorController:
    def __init__(self) -> None:
        self.isOpen=False
        self.time=2
        self.OPEN=5
        self.CLOSE=7
        self.flush=lambda : GPIO.cleanup() 

    def open(self):
        self.isOpen=True
        GPIO.setup(self.OPEN,GPIO.OUT)
        GPIO.output(self.OPEN,True)
        sleep(self.time)
        GPIO.output(self.OPEN,False)
        return

    def close(self):
        self.isOpen=False
        GPIO.setup(self.CLOSE,GPIO.OUT)
        GPIO.output(self.CLOSE,True)
        sleep(self.time)
        GPIO.output(self.CLOSE,False)
        return