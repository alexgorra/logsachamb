import logging
import time
import serial


from Configurations import commands, settings
from Server.server_mapper import command_mapper

log = logging.getLogger("Logger")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)

class Controller:

    def __init__(self):
        self.log = log

    def execute(self, mapped_command: str) -> dict:

        if(mapped_command == "CONNECT"):
            self.connect_to_controller()
            
        if(mapped_command == "DISCONNECT"):
            self.disconnect_to_controller()
        

        # Placeholder for future serial communication logic.
        self.log.info(f"Executing mapped command: {mapped_command}")
        # Simulated response 
        return {
            "executed": True,
            "gcode": mapped_command,
            "controller_message": "Simulated execution OK"
        }
    

    #Controller functions

    def connect_to_controller(self):
        # Initialize serial connection
        try:
            self.serial_connection = serial.Serial(settings.COM_PORT, settings.BAUD_RATE, timeout=1)
        except Exception as e:
            self.log.error(f"Error connecting to the controller: {e}")

    def disconnect_to_controller(self):
        try:
            self.serial_connection.close()
        except Exception as e:
            self.log.error(f"Error disconnecting to the controller: {e}")

    def send_command(self, mapped_command: str):
        try:
            self.serial_connection.write(f"{mapped_command}\n".encode('utf-8'))
            self.log.info(f"Sent command to controller: {mapped_command}")
        except Exception as e:
            self.log.error(f"Error sending command to controller: {e}")

    def get_current_position(self):
        try:
            self.serial_connection.write(b'?\n')
            time.sleep(0.1)
            response = self.serial_connection.readline().decode('utf-8').strip()
            # Parse: "<Idle|WPos:1.234,5.678,0.000,9.012"
            if 'WPos:' in response:
                pos_str = response.split('WPos:')[1].split('>')[0]
                coords = [float(x) for x in pos_str.split(',')[:3]]  # X,Y,A
                return coords
            return None
        except:
            return None

    def is_near_zero(self, position, tolerance=0.01):
        if position is None:
            return False
        
        return all(abs(coord) < tolerance for coord in position)
    
    def save_zero(self):

        try:
            zero_command = 'G10 P1 L20 X0 Y0 A0\n'

            self.serial_connection.write(zero_command.encode('utf-8'))
            time.sleep(0.2)

            # Writes in case we want to check
            self.serial_connection.write(b'?\n')
            self.serial_connection.write(b'$gcode\n')

            self.disconnect_to_controller()
            logging.info("Disconnected")
            time.sleep(2)
            logging.info("Connecting")
            self.connect_to_controller()
            logging.info("Connected")

            self.serial_connection.write(zero_command.encode('utf-8'))

            self.serial_connection.write(b'?\n')
            time.sleep(0.2)
            where = self.serial_connection.read_all().decode('utf-8')
            logging.info(where)
            self.serial_connection.write(b'$gcode\n')
            time.sleep(0.2)
            offsets = self.serial_connection.read_all().decode('utf-8')
            logging.info(offsets)

        except Exception as e:
            logging.error("Error saving zero position: %s", e)




controller = Controller()
