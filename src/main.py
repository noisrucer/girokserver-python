from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check():
    return {"message": "I'm doing fine, thanks for asking"}
