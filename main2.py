from fastapi import FastAPI, WebSocket, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import cv2
import base64


app = FastAPI()
# html파일을 서비스할 수 있는 jinja설정 (/templates 폴더사용)
templates = Jinja2Templates(directory="templates")


# 웹소켓 연결을 테스트 할 수 있는 웹페이지 (http://127.0.0.1:8000/client)
@app.get("/client")
async def client(request: Request):
    # /templates/client.html파일을 response함
    return templates.TemplateResponse("client.html", {"request":request})


# 웹소켓 설정 ws://127.0.0.1:8000/ws 로 접속할 수 있음
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    try:
        print(f"client connected : {websocket.client}")
        await websocket.accept() # client의 websocket접속 허용
        await websocket.send_text(f"Welcome client : {websocket.client}")
        
        # Receive the video file link from the client
        video_link = await websocket.receive_text()
        if not video_link:
            raise ValueError("Empty video link received")
        print("Received video link:", video_link)

        # Attempt to open the video file for processing
        cap = cv2.VideoCapture(video_link)
        if not cap.isOpened():
            raise IOError("Failed to open video file: " + video_link)
        
        frame_count = 0
        isProcessing = False
        processing_delay = 0.5  # Simulated delay between sending responses (adjust as needed)

        while True:
            # Check if the server is still processing the previous frame
            if isProcessing:
                await asyncio.sleep(processing_delay)
                continue

            # Read a frame from the video
            ret, frame = cap.read()
            if not ret:
                break

            # Set the processing flag to indicate that the server is busy
            isProcessing = True

            frame_count += 1

            # Encode the frame as base64
            _, frame_data = cv2.imencode('.jpg', frame)
            base64_frame = base64.b64encode(frame_data).decode("utf-8")


            # Send the base64-encoded frame to the client
            await websocket.send_text(base64_frame)
            # Simulate processing delay
            await asyncio.sleep(processing_delay)
            print("test")
            print("ㅋㅋ")

            # Reset the processing flag once frame processing is complete
            isProcessing = False

        # Close the video file and connection when finished
        cap.release()
        print("Video processing complete. Closing connection.")
        await websocket.close()

    except Exception as e:
        print(f"Error on the server: {str(e)}")