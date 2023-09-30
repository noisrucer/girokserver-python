from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.auth.routers import router as auth_router
from src.application.event_category.routers import router as event_category_router
from src.infrastructure.database.connection import Base, engine
from src.infrastructure.exceptions.handlers import base_custom_exception_handler
from src.shared.exceptions import BaseCustomException

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(event_category_router, prefix="/api/v1")
app.add_exception_handler(BaseCustomException, base_custom_exception_handler)


@app.get("/")
def health_check():
    return {"message": "I'm doing fine, thanks for asking"}
