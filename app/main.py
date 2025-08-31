from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import generate, parse
import os


app = FastAPI(title="AI Resume + Cover Letter Generator API")


origins = (os.getenv("ALLOWED_ORIGINS") or "http://localhost:5173").split(",")
app.add_middleware(
CORSMiddleware,
allow_origins=[o.strip() for o in origins],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


app.include_router(generate.router)
app.include_router(parse.router)


@app.get("/")
def root():
  return {"status": "ok"}