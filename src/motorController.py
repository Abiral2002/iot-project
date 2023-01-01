# Code for motor
class MotorController:
    def __init__(self) -> None:
        self.isOpen=False

    def open(self):
        self.isOpen=True
        pass

    def close(self):
        self.isOpen=False
        pass