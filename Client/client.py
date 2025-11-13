# WebClient/client.py
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

class Client:
    def __init__(self, server_url="http://127.0.0.1:8000/commands"):
        self.log = logging.getLogger("ClientLogger")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.INFO)
        
        self.app = FastAPI()
        # Get the directory where this file is located
        client_dir = Path(__file__).parent
        templates_dir = client_dir / "templates"
        self.templates = Jinja2Templates(directory=str(templates_dir))
        self.server_url = server_url
        self.data = None

        # --- Define routes ---
        @self.app.get("/", response_class=HTMLResponse)
        async def main_page(request: Request):
            """Render the web interface."""
            return self.templates.TemplateResponse("control.html", {"request": request})

        @self.app.post("/send")
        async def send_command(command: str = Form(...)):
            """Send a command to the backend server."""
            return await self.send_command(command)

        @self.app.get("/last")
        async def get_last_command():
            """Fetch the last command from the backend server."""
            return await self.read_last_command()

        self.log.info("Web client initialized")

    async def send_command(self, command: str):
        """POST a command to the server."""
        self.log.info(f"Sending command to server: {command}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.server_url, json={"command": command})
            self.log.info(f"Response from server: {response.text}")
            return {"status": "ok", "server_response": response.json()}
        except Exception as e:
            self.log.error(f"Error sending command: {e}")
            return {"status": "error", "error": str(e)}

    async def read_last_command(self):
        """GET the last command from the server."""
        try:
            self.log.info("Requesting last command from server")
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.server_url}/last")
                data = response.json()
                self.data = data
                self.log.info(f"Received last command: {data}")
                return {"server_response": data}
        except Exception as e:
            self.log.error(f"Error reading command: {e}")
            return {"error": str(e)}

client = Client()
app = client.app