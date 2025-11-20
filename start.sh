#!/bin/bash
# Start server in the background
uvicorn Server.server:app --host 0.0.0.0 --port 8000 &

# Start client in the foreground
uvicorn Client.client:app --host 0.0.0.0 --port 8080
