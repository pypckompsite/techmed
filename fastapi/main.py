from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from auth import auth_router
app = FastAPI()


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