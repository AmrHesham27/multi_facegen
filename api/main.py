from fastapi import FastAPI, HTTPException
import uuid
import os
from middlewares.KeyMiddleware import KeyMiddleware
from requests.FacegenRequest import FacegenRequest 
from controllers.FacegenController import FacegenController
from helpers import restart_comfyui_servers
import asyncio

app = FastAPI()

app.add_middleware(KeyMiddleware)

## ImageEditing - Facegen
@app.post("/api/create/facegen")
async def facegen(request: FacegenRequest):
    try:
        return await asyncio.wait_for(FacegenController.create(request), timeout = 300)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out")

## Restart Server
@app.post("/api/restart")
async def restart_server():
    return await restart_comfyui_servers()

@app.post("/api/test")
async def test():
    return {"message": "Hello, World!"}
