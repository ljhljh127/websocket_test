from fastapi import APIRouter,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import server
import client

import asyncio
import websockets
import cv2
import base64

WEB_URL = "http://localhost:8000"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[WEB_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RTSPRequest(BaseModel):
    rtsp_url: str

@app.post("/")
async def create_rtspsession(rtsp_request: RTSPRequest):
    rtsp_url = rtsp_request.rtsp_url
    asyncio.create_task(server.start_server())
    frame=asyncio.create_task(client.start_client())
    print(frame)
    return {"frame": frame}


@app.post("/test")
def test2():
    print("하이")



