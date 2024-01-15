from .camera import WebCamVideoStream
class WebStream():

    def __init__(self):
        self.matched=True
        self.cam=WebCamVideoStream()

    def streams(self):
        try:
            image=self.cam.read()
            return image.tobytes()
        except Exception as e:
            self.cam.close()
            return False

    def camera(self):        
        return self.streams()
            