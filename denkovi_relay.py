import serial
import time


class DenkoviRelay:
    def __init__(self, port, baud_rate=9600):
        """Initialize Denkovi relay controller.

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

    def disconnect(self):
        """Disconnect from the relay controller."""
        if self.ser:
            self.ser.close()
            self.ser = None

    def set_pattern(self, pattern):
        """Set relay pattern from a binary string.

        Args:
            pattern (str): Binary pattern like '10101010' for 8 relays
                          or '1010101010101010' for 16 relays
        """
        if not self.ser:
            raise RuntimeError("Not connected. Call connect() first.")

        # Remove any spaces or separators
        pattern = pattern.replace(" ", "").replace("_", "")

        # Validate pattern length
        if len(pattern) not in [8, 16]:
            raise ValueError("Pattern must be 8 or 16 bits long")

        # Convert binary string to integer
        value = int(pattern, 2)

        # Send the command
        if len(pattern) == 8:
            # Single byte for 8 relays
            self.ser.write(bytes([value]))
        else:
            # Two bytes for 16 relays                        This is untested so prolly wrong!!!!!!
            # Split into two 8-bit values
            low_byte = value & 0xFF  # First 8 bits
            high_byte = (value >> 8) & 0xFF  # Last 8 bits
            self.ser.write(bytes([low_byte, high_byte]))

        time.sleep(0.1)


# Example usage:
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python denkovi_relay.py <port> <pattern>")
        print("Example (8 relays): python denkovi_relay.py COM8 10101010")
        print("Example (16 relays): python denkovi_relay.py COM8 1010101010101010")
        sys.exit(1)

    port = sys.argv[1]
    pattern = sys.argv[2]

    relay = DenkoviRelay(port)
    try:
        relay.connect()
        relay.set_pattern(pattern)
    finally:
        relay.disconnect()
