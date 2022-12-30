# Code for motor
class MotorController:
    def __init__(self) -> None:
        self.isOpen=True

    def open(self):
        self.isOpen=True
        pass

    def close(self):
        self.isOpen=False
        pass