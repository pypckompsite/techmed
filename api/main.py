from fastapi import FastAPI, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware

from api.admin import admin_router
from api.auth import auth_router
from api.misc import misc_router


from api.doctor.main import doctor_router
from api.patient.main import patient_router
app = FastAPI(
    title="TECHMED",
    description="This web application is designed to streamline the medical appointment process. The app's main feature is the use of speech-to-text (STT) technology to transcribe appointments in real-time, and AI to transform those transcripts into a detailed appointment report.",
    version='0.0.1',
    servers=[{"url": "http://localhost:8000", "description": "Local server"}]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return 'Hello World!'


#Actions related to auth
app.include_router(auth_router, prefix="/auth")

# Actions reserved for admin
app.include_router(admin_router, prefix="/admin")

# Misc actions like listing enum types, displaying publicly available info, functions that are shared between user types
app.include_router(misc_router, prefix="/misc")

# Actions reserved for doctors
app.include_router(doctor_router, prefix="/doctor")
#
# # Actions reserved for patients
# app.include_router(patient_router, prefix="/patient")