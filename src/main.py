from fastapi import FastAPI
from email_validator import EmailNotValidError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.database import engine
from src.auth.router import router as auth_router
from src.category.router import router as category_router
from src.task.router import router as task_router
import src.user.models as user_models
import src.auth.models as auth_models

user_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(task_router)

@app.get("/")
async def root():
    return {"message": "hello to the root"}