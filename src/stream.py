from .camera import WebCamVideoStream

class WebStream():
    def __init__(self):
        self.matched=True

    async def camera(self,response):
        if not self.matched:
            await response.send_text("Access denied")
            return
        stream=WebCamVideoStream()
        while self.matched:
            image=stream.read()
            await response.send_bytes(image.tobytes())
        return "Stream Closed"