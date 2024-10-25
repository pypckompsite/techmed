from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from admin import admin_router
from auth import auth_router
app = FastAPI(
    title="TECHMED",
    description="This web application is designed to streamline the medical appointment process. The app's main feature is the use of speech-to-text (STT) technology to transcribe appointments in real-time, and AI to transform those transcripts into a detailed appointment report.",
    version='0.0.1',

)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return "Hello World!"

# @app.on_event("startup")
# def on_startup():
#     init_db()

app.include_router(auth_router, prefix="/auth")
app.include_router(admin_router, prefix="/admin")