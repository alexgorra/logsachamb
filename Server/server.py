import logging
from fastapi import FastAPI
from pydantic import BaseModel
from Server.server_mapper import command_mapper
from Server.server_controller import controller
from Configurations import settings


# --- Logging setup ---
log = logging.getLogger("Logger")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)


class Command(BaseModel):
    command: str

class Server:
    def __init__(self):
        self.log = log
        self.app = FastAPI()
        self.last_command = None  # raw command key received
        self.last_mapped_command = None  # translated g-code
        self.last_controller_response = None  # response dict from controller
        self.command_history_list = []

        # Root route
        @self.app.get("/")
        def read_root():
            return {
                "message": "Welcome to server.py",
                "Command History": list(reversed(self.command_history_list))
            }

        # POST route to receive a command
        @self.app.post("/commands")
        async def receive_command(cmd: Command):
            # Receives Command
            self.last_command = cmd.command
            self.log.info(f"Received command key: {cmd.command}")

            # Verifies Command
            mapped = command_mapper.map_command(cmd.command)
            if mapped == "":  # mapper returns empty string when unknown
                return {"status": "error", "error": f"Unknown command '{cmd.command}'"}
            self.last_mapped_command = mapped

            #Executa (simulado)
            controller_resp = controller.execute(mapped)
            self.last_controller_response = controller_resp

            self.command_history_list.append({cmd.command: mapped})

            # 4. Return aggregated response to client
            return {
                "status": "ok",
                "received_command": cmd.command,
                #"mapped_command": mapped,
                #"controller_response": controller_resp, #parse later
            }

        # GET route to read the last command received
        @self.app.get("/commands/last")
        async def get_last_command():
            if not self.last_command:
                return {"message": "No command received yet."}
            return {
                "last_command": self.last_command,
                "last_mapped_command": self.last_mapped_command,
                "last_controller_response": self.last_controller_response,
            }

        self.log.info("Server initialized")


server = Server()
app = server.app
