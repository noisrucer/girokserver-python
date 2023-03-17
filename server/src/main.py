from fastapi import FastAPI
from email_validator import EmailNotValidError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from server.src.database import engine
from server.src.auth.router import router as auth_router
from server.src.category.router import router as category_router
from server.src.task.router import router as task_router
import server.src.user.models as user_models

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