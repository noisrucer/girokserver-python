from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.auth.routers import router as auth_router
from src.application.event.routers import router as event_router
from src.application.event_category.routers import router as event_category_router
from src.infrastructure.database.connection import Base, engine
from src.infrastructure.exceptions.handlers import add_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(event_category_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")
add_exception_handlers(app)


@app.get("/")
def health_check():
    return {"message": "I'm doing fine, thanks for asking"}
