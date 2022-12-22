import cv2

class WebCamVideoStream():
    def __init__(self):
        self.stream=cv2.VideoCapture(0)
        (self.rate,self.frame)=self.stream.read()
        self.open=True

    def update(self):
        if self.open:
            (self.rate,self.frame)=self.stream.read()
            self.convertTomp4()
            return (self,self.out.read())

    def convertTomp4(self):
        out_forurcc=cv2.VideoWriter_fourcc(*"mp4")
        self.out=cv2.VideoWriter("./../cameraBuff/buff.mp4",out_forurcc,30,(640,480))
        self.out.write(self.frame)

    def close(self):
        self.open=False
        self.out.close()