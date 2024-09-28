#!/bin/sh

# Set default port if not provided
PORT=${PORT:-8000}


# Start the FastAPI app
uvicorn api:app --host 0.0.0.0 --port $PORT