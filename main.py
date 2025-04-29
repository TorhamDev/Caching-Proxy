import argparse
import json

import uvicorn
from fastapi import FastAPI, Request

from modules.redis_db import RedisDB

app = FastAPI()
redis = RedisDB()


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
async def catch_all(request: Request, path: str):
    """
    This endpoint catches all incoming requests and acts as a proxy.
    It demonstrates how to access the requested path and method.
    """

    cache_key = f"{request.method}::{path}::{target_address}"

    cached_data = redis.get(cache_key)
    if cached_data:
        return {"message": "Cache got hit."}

    cache_data = {
        "method": request.method,
        "path": path,
        "body": (await request.body()).decode(),
        "headers": dict(request.headers),
        "Origin": target_address,
    }

    redis.set(key=cache_key, value=json.dumps(cache_data))

    return {"message": "Not cache found. saving the result."}


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

    # running wenserver
    target_address = args.origin
    uvicorn.run(app, host="0.0.0.0", port=args.port)

    # clos redis connection after program terminated
    redis.close()
