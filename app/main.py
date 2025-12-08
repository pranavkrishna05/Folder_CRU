from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db

app = FastAPI(title="Folder_CRU API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Folder_CRU Backend Active"}
