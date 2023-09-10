from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.user.models as user_models
from src.auth.router import router as auth_router
from src.category.router import router as category_router
from src.database import engine
from src.task.router import router as task_router

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
