#!/usr/bin/env python3
# Client with both Web UI and CLI support
import logging
import sys
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx


class Client:
    def __init__(self, server_url="http://10.128.3.114:8000"):
        self.log = logging.getLogger("ClientLogger")
        # Clear existing handlers to prevent duplicates
        self.log.handlers.clear()
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.INFO)
        
        self.app = FastAPI()
        client_dir = Path(__file__).parent
        templates_dir = client_dir / "templates"
        self.templates = Jinja2Templates(directory=str(templates_dir))
        self.server_url = server_url

        # Web interface
        @self.app.get("/", response_class=HTMLResponse)
        async def main_page(request: Request):
            return self.templates.TemplateResponse("control.html", {"request": request})

        # Send command endpoint
        @self.app.post("/send")
        async def send_command(command: str = Form(...)):
            return await self.send_cmd(command)

        self.log.info("Client ready")

    async def send_cmd(self, command: str):
        """Send command to server (used by both web and CLI)"""
        self.log.info(f"Sending: {command}")
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.server_url}/cmd/{command}")
            self.log.info(f"Response: {response.text}")
            return response.json()
        except (httpx.ConnectError, httpx.TimeoutException):
            self.log.error("Server offline")
            return {"ok": False, "error": "Server offline"}
        except Exception as e:
            self.log.error(f"Error: {e}")
            return {"ok": False, "error": str(e)}


# CLI mode
async def cli_mode():
    """Run in CLI mode to send a single command"""
    if len(sys.argv) < 2:
        print("Usage: python Client/client.py <command>")
        print("\nExamples:")
        print("  python Client/client.py x_plus_1")
        print("  python Client/client.py 'G0 X10 Y20'")
        print("  python Client/client.py G0 X10 Y20")
        sys.exit(1)
    
    # Join all arguments to support commands with spaces
    command = " ".join(sys.argv[1:])
    client = Client()
    
    try:
        result = await client.send_cmd(command)
        print(f"Response: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# Initialize client for web mode
client = Client()
app = client.app


# Entry point - detect CLI vs web mode
if __name__ == "__main__":
    # CLI mode - send command and exit
    asyncio.run(cli_mode())
else:
    # Web mode - imported by uvicorn
    pass