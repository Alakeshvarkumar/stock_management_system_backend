from fastapi import FastAPI

from app.routes import router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "Creation succeed"}

app.include_router(router)