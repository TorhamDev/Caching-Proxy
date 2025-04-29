import argparse

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    """
    A simple root endpoint that returns a greeting.
    """
    return {"message": "Hello, this is your basic FastAPI server!"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Caching Proxy",
        description="Cache Your Requests.",
        epilog="type --help for more help.",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port that cache server will run on.",
    )

    parser.add_argument(
        "-r",
        "--origin",
        type=str,
        required=True,
        help="Target address that cache server will work with.",
    )

    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)
