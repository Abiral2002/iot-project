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
            return self.read()

    def read(self,stream):
        self.update()
        _,image=cv2.imencode(".jpg",self.frame)
        return image

    def close(self):
        self.open=False
        self.stream.release()

# def cameraControler():
#     webCam=WebCamVideoStream()
#     webCam