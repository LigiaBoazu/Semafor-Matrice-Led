from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from .device.display import scroll_message, display_static_message
import asyncio
from threading import Lock

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

semaphore_state = "VERDE"
remaining_time = 60
lock = Lock()

async def manage_semaphore():
    global semaphore_state, remaining_time
    while True:
        await asyncio.sleep(1)
        with lock:
            remaining_time -= 1
            if remaining_time <= 0:
                if semaphore_state == "VERDE":
                    semaphore_state = "ROSU"
                else:
                    semaphore_state = "VERDE"
                display_static_message(semaphore_state)
                remaining_time = 60

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(manage_semaphore())

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with lock:
        state = semaphore_state
        time_left = remaining_time
    return templates.TemplateResponse("index.html", {"request": request, "state": state, "remaining_time": time_left})

@app.post("/display")
async def display_message(message: str = Form(...)):
    global semaphore_state
    await scroll_message(message)
    with lock:
        display_static_message(semaphore_state)
    return JSONResponse({"message": f"Message displayed: {message}"})

@app.post("/set_state")
async def set_state(state: str = Form(...)):
    global semaphore_state, remaining_time
    with lock:
        semaphore_state = state
        remaining_time = 60
    display_static_message(semaphore_state)
    return JSONResponse({"message": f"Semaphore set to: {state}"})

@app.get("/remaining_time")
async def get_remaining_time():
    with lock:
        time_left = remaining_time
    return JSONResponse({"remaining_time": time_left})
