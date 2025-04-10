import serial
import time


class Denkovi16Relay:
    def __init__(self, port, baud_rate=9600):
        """Initialize Denkovi 16-relay controller.

        Args:
            port (str): COM port name (e.g., 'COM8')
            baud_rate (int): Baud rate (default 9600)
        """
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None

    def connect(self):
        """Connect to the relay controller."""
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        # Send wake-up command
        self.ser.write(b"ask//")
        time.sleep(0.1)  # Give the board time to process the command

    def disconnect(self):
        """Disconnect from the relay controller."""
        if self.ser:
            self.ser.close()
            self.ser = None

    def get_status(self):
        """Get status of all relays.

        Returns:
            list: List of 16 boolean values indicating relay states (True=ON, False=OFF)
        """
        if not self.ser:
            raise RuntimeError("Not connected. Call connect() first.")

        self.ser.write(b"ask//")
        time.sleep(0.005)  # 5ms minimum interval between commands

        # Read 2 bytes response
        response = self.ser.read(2)
        if len(response) != 2:
            raise RuntimeError("Failed to read relay status")

        # Convert bytes to relay states
        states = []
        # First byte contains relays 1-8 (bit7 = relay1, bit0 = relay8)
        byte1 = response[0]
        for i in range(7, -1, -1):
            states.append(bool(byte1 & (1 << i)))

        # Second byte contains relays 9-16 (bit7 = relay9, bit0 = relay16)
        byte2 = response[1]
        for i in range(7, -1, -1):
            states.append(bool(byte2 & (1 << i)))

        return states

    def set_relay(self, relay_num, state):
        """Set single relay state.

        Args:
            relay_num (int): Relay number (1-16)
            state (bool): True for ON, False for OFF
        """
        if not self.ser:
            raise RuntimeError("Not connected. Call connect() first.")

        if not 1 <= relay_num <= 16:
            raise ValueError("Relay number must be between 1 and 16")

        # Convert relay number to two-digit string (01-16)
        addr = f"{relay_num:02d}"
        # Create command: addr1 + addr2 + sign + //
        cmd = addr[0].encode() + addr[1].encode() + (b"+" if state else b"-") + b"//"

        self.ser.write(cmd)
        time.sleep(0.005)  # 5ms minimum interval between commands

    def set_all_relays(self, state):
        """Set all relays ON or OFF.

        Args:
            state (bool): True for ON, False for OFF
        """
        if not self.ser:
            raise RuntimeError("Not connected. Call connect() first.")

        cmd = b"on//" if state else b"off//"
        self.ser.write(cmd)
        time.sleep(0.005)  # 5ms minimum interval between commands

    def set_pattern(self, pattern):
        """Set relay pattern from a binary string.

        Args:
            pattern (str): Binary pattern like '1010101010101010' for 16 relays
        """
        if not self.ser:
            raise RuntimeError("Not connected. Call connect() first.")

        # Remove any spaces or separators
        pattern = pattern.replace(" ", "").replace("_", "")

        # Validate pattern length
        if len(pattern) != 16:
            raise ValueError("Pattern must be 16 bits long for 16-relay board")

        # Convert binary string to two bytes
        value = int(pattern, 2)
        byte1 = (value >> 8) & 0xFF  # First byte for relays 1-8
        byte2 = value & 0xFF  # Second byte for relays 9-16

        # Create command: 'x' + byte1 + byte2 + '//'
        cmd = b"x" + bytes([byte1, byte2]) + b"//"

        self.ser.write(cmd)
        time.sleep(0.005)  # 5ms minimum interval between commands


# Example usage:
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python denkovi_16_relay.py <port> <pattern>")
        print("Example: python denkovi_16_relay.py COM8 1010101010101010")
        sys.exit(1)

    port = sys.argv[1]
    pattern = sys.argv[2]

    relay = Denkovi16Relay(port)
    try:
        relay.connect()
        relay.set_pattern(pattern)
    finally:
        relay.disconnect()
