from fastapi import FastAPI, WebSocket
from .stream import WebStream
from fastapi.responses import RedirectResponse

app=FastAPI()


stream=WebStream()

@app.get("/")
def home():
    return "Hello World"

@app.post("/login")
def login(password:str):
    if password!=open("./../masterpassword.txt","r").read().strip():
        return {"msg":"Wrong Password access Denied"}
    stream.matched=True
    return RedirectResponse("/camera")

@app.websocket("/camera")
async def camera(websocket: WebSocket):
    await waitRes(websocket)
    closed=await stream.camera(websocket)
    if closed:
        websocket.close()
        return {"msg":"Stream closed"}

async def waitRes(websocket: WebSocket):
    message=await websocket.receive()
    if message=="Stop":
        stream.matched=False
    