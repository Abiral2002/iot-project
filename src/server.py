from fastapi import FastAPI, WebSocket, Response
from fastapi.middleware.cors import CORSMiddleware
from .stream import WebStream
from .motorController import MotorController
import os
import asyncio
from collections import deque
import secrets
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

class Password(BaseModel):
    password: str



app = FastAPI()
app.mount("/static",StaticFiles(directory=os.path.abspath("./frontEnd")),name="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
connectedDevice= deque()
stream = WebStream()
motor = MotorController()
cookies = []

def runCamera(queue):
    stream.camera(queue)

@app.post("/login")
def login(response: Response, password: Password):
    if password.password != open(os.path.join(os.getcwd(), "src/masterpassword.txt"), "r").read().strip():
        return {"msg": "Wrong Password access Denied"}
    secret = secrets.token_hex(10)
    cookies.append(secret)
    
    response.set_cookie("code", secret, 24*60*60*60)
    return {"msg":"success"}

@app.websocket("/camera")
async def camera(websocket: WebSocket):
    print(websocket.cookies)
    try:
        if not websocket.cookies["code"] in cookies:
            return "Not logged in"
        await asyncio.sleep(0)
        await websocket.accept()
        connectedDevice.append(websocket)
        while True:
            await asyncio.sleep(0)
            while connectedDevice:
                try:
                    await asyncio.sleep(0)
                    sock=connectedDevice.popleft()
                    await sock.send_bytes(stream.camera())
                    connectedDevice.append(sock)
                except:
                    pass
    except KeyError:
        return {"msg":"No cookie found"}


@app.get("/open-lock")
def open_lock():
    if not motor.isOpen:
        motor.open()
        return {"msg": "Lock opened"}
    return {"msg": "Lock was opened"}


@app.get("/close-lock")
def close_lock():
    if motor.isOpen:
        motor.close()
        return {"msg": "Lock closed"}
    return {"msg": "Lock was closed"}


@app.get("/status")
def status():
    if motor.isOpen:
        return {"msg": "Open"}
    else:
        return {"msg": "closed"}