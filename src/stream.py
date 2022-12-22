from .camera import WebCamVideoStream

class WebStream():
    def __init__(self):
        self.matched=False

    def camera(self,response):
        if not self.matched:
            response.send("Access denied")
            return
        stream=WebCamVideoStream()
        while self.matched:
            image=stream.read()
            response.send(image.tobytes())
        response.send("Stream Closed")