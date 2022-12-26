from .camera import WebCamVideoStream
from fastapi import WebSocket
import time

class WebStream():
    def __init__(self):
        self.matched=True

    async def camera(self,websocket:WebSocket):
        if not self.matched:
            await websocket.close(reason="Access denied")
            return
        stream=WebCamVideoStream()
        await websocket.accept()
        while True:
            try:
                image=stream.read()
                time.sleep(0.01)
                await websocket.send_bytes(image.tobytes())
            except:
                stream.close()
                break
        # print("Stream closed")