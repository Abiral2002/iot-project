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
    await stream.camera(websocket)

async def waitRes(websocket: WebSocket):
    message=await websocket.recv()
    if message=="Stop":
        stream.matched=False
    