from fastapi import FastAPI
import uvicorn

app = FastAPI()
#comment 
@app.get("/")
def read_root():
    return "Hello World!"