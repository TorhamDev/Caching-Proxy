import argparse

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
async def catch_all(request: Request, path: str):
    """
    This endpoint catches all incoming requests and acts as a proxy.
    It demonstrates how to access the requested path and method.
    """
    print("Received request:")
    print(f"  Method: {request.method}")
    print(f"  Path: /{path}")
    print(f"  Headers: {request.headers}")

    return {
        "message": f"Request received for path: /{path} with method: {request.method}"
    }


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
