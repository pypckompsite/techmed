from fastapi import FastAPI, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware

from admin import admin_router
from auth import auth_router
from misc import misc_router
app = FastAPI(
    title="TECHMED",
    description="This web application is designed to streamline the medical appointment process. The app's main feature is the use of speech-to-text (STT) technology to transcribe appointments in real-time, and AI to transform those transcripts into a detailed appointment report.",
    version='0.0.1',
    servers=[{"url": "http://localhost:8000", "description": "Local server"}]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return 'Hello World!'



app.include_router(auth_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")
app.include_router(misc_router, prefix="/misc")