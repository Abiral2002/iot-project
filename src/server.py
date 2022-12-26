from fastapi import FastAPI, WebSocket
from .stream import WebStream
from .motorController import MotorController
from fastapi.responses import RedirectResponse

app=FastAPI()


stream=WebStream()
motor=MotorController()

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
    await stream.camera(websocket)

@app.get("/open-lock")
def open_lock():
    if not motor.isOpen:
        motor.open()
        return {"msg":"Lock opened"}

@app.get("/close-lock")
def close_lock():
    if motor.isOpen:
        motor.close()
        return {"msg":"Lock closed"}

@app.get("/status")
def status():
    if motor.isOpen:
        return {"msg":"Open"}
    else:
        return {"msg":"closed"}