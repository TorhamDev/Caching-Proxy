from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def read_root():
    """
    A simple root endpoint that returns a greeting.
    """
    return {"message": "Hello, this is your basic FastAPI server!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
