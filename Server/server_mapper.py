import logging

from Configurations import commands, settings
log = logging.getLogger("Logger")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)

class CommandMapper:

    def __init__(self):
        self.log = log

    def map_command(self, command: str) -> str:
        # Validate membership explicitly (previous logic always evaluated truthy)
        if (
            command in commands.COMMANDS_X
            or command in commands.COMMANDS_Y
            or command in commands.COMMANDS_A
            or command in commands.COMMANDS_SPECIAL
        ):
            if command in commands.COMMANDS_X:
                mapped_command = commands.COMMANDS_X[command]
            elif command in commands.COMMANDS_Y:
                mapped_command = commands.COMMANDS_Y[command]
            elif command in commands.COMMANDS_A:
                mapped_command = commands.COMMANDS_A[command]
            else:
                mapped_command = commands.COMMANDS_SPECIAL[command]

            self.log.info(f"Mapped command '{command}' to '{mapped_command}'")
            return mapped_command
        else:
            self.log.warning(f"The command '{command}' is not recognized. (check commands.py)")
            return ""


command_mapper = CommandMapper()
