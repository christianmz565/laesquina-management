from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import api_app
from fastapi.middleware.cors import CORSMiddleware
from .env import FILES_PATH
from .database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(FILES_PATH, exist_ok=True)
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/api", api_app)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
