import logging
from fastapi import FastAPI
from Server.server_mapper import command_mapper
from Server.server_controller import controller


# --- Logging setup ---
log = logging.getLogger("Logger")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)


class Server:
    def __init__(self):
        self.log = log
        self.app = FastAPI()
        self.history = []

        # Root - show history
        @self.app.get("/")
        def root():
            return {"history": list(reversed(self.history))}

        # Simple GET endpoint - just send command in URL
        @self.app.get("/cmd/{command}")
        async def send_cmd(command: str):
            self.log.info(f"Command: {command}")
            
            # Map command if exists in mapper, otherwise use raw
            mapped = command_mapper.map_command(command) or command
            
            # Execute
            controller.execute(mapped)
            
            # Save to history
            self.history.append({"command": command, "mapped": mapped})
            
            return {"ok": True, "command": command, "mapped": mapped}

        # POST route to accept JSON payloads for compatibility
        @self.app.post("/commands")
        async def post_commands(payload: dict):
            """Accept JSON body {"command": "..."} and process it."""
            command = payload.get("command") if isinstance(payload, dict) else None
            if not command:
                return {"ok": False, "error": "missing 'command' field"}

            self.log.info(f"Command (POST): {command}")
            mapped = command_mapper.map_command(command) or command
            controller.execute(mapped)
            self.history.append({"command": command, "mapped": mapped})
            return {"ok": True, "command": command, "mapped": mapped}

        self.log.info("Server ready")


server = Server()
app = server.app
