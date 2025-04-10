import serial
import serial.tools.list_ports
import time
import sys


def list_com_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port.device} - {port.description}")


def send_command(ser, command):
    print(f"CMD: {command.hex()}")
    ser.write(command)
    time.sleep(0.1)


def test_relays(port_name, baud_rate=9600):
    try:
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Testing {port_name} at {baud_rate} baud")

        send_command(ser, b"ask//")

        # Test each relay (bit 0-7)
        for relay in range(8):
            print(f"\nRelay {relay} ON")
            send_command(ser, bytes([1 << relay]))
            input()

            print(f"\nRelay {relay} OFF")
            send_command(ser, bytes([0]))
            input()

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if "ser" in locals():
            ser.close()


if __name__ == "__main__":
    print("Available ports:")
    list_com_ports()

    if len(sys.argv) != 2:
        print("Usage: python main.py <port>")
        print("Example: python main.py COM8")
        sys.exit(1)

    port = sys.argv[1]
    baud = 9600
    test_relays(port, baud)
